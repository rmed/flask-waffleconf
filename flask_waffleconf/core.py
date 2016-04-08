# -*- coding: utf-8 -*-
#
# Flask-WaffleConf - https://github.com/rmed/flask-waffleconf
#
# Copyright (C) 2015, 2016  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from . import util

# Imports for multiprocess deployments
# gevent is optional
try:
    import gevent
    import gevent.monkey
    gevent.monkey.patch_all()

except ImportError:
    pass

# Redis is required for notifying other processes
try:
    import redis
    import time
    import threading
    _MULTIPROC = True

except ImportError:
    _MULTIPROC = False


class _WaffleState(object):
    """ Store configstore for the app state.

        Params:

            app         - Flask application instance
            configstore - WaffleStore instance

        This object will update its application's configuration and if the
        `WAFFLE_MULTIPROC` setting is set to True, it will also notify other
        processes using Redis channel.
    """

    def __init__(self, app, configstore):
        self.app = app
        self.configstore = configstore

        if self.app.config.get('WAFFLE_MULTIPROC', False) and _MULTIPROC:
            # Multiprocess update notification
            self._tstamp = time.time()

            self._listener = threading.Thread(target=self._listen_updates)
            self._listener.setDaemon(True)
            self._listener.start()

        # Get configs from database
        parsed = self.parse_conf()

        if not parsed:
            return None

        # Update app config
        self.app.config.update(parsed)

    def _listen_updates(self):
        """ Listen to redis channel for a configuration update notification
            using pub/sub.
        """
        r = redis.client.StrictRedis(
            host=self.app.config.get('WAFFLE_REDIS_HOST', 'localhost'),
            port=self.app.config.get('WAFFLE_REDIS_PORT', 6379))

        sub = r.pubsub(ignore_subscribe_messages=True)
        sub.subscribe(self.app.config.get('WAFFLE_REDIS_CHANNEL', 'waffleconf'))

        while True:
            for msg in sub.listen():
                # Skip non-messages
                if not msg['type'] == 'message':
                    continue

                tstamp = float(msg['data'])

                # Compare timestamps and update config if needed
                if tstamp > self._tstamp:
                    configs = self.app.config.get('WAFFLE_CONFS', {})
                    parsed = self._parse_conf(configs)

                    self.app.config.update(parsed)
                    self._tstamp = tstamp

    def parse_conf(self, keys=[]):
        """ Parse configuration values from the database specified in the
            `keys` argument. The extension must have been previously
            initialized!

            If a key is not found in the database, it will be created with the
            default value specified.

            Params:

                confs - list of keys to parse. If the list is empty, then
                        all the keys known to the application will be used.

            Returns:

                result - dict of the parsed config values
        """
        confs = self.app.config.get('WAFFLE_CONFS', {})
        if not keys:
            keys = confs.keys()

        result = {}

        for key in keys:
            # Some things cannot be changed...
            if key.startswith('WAFFLE_'):
                continue

            # No arbitrary keys
            if key not in confs.keys():
                continue

            stored_conf = self.configstore.get(key)

            if not stored_conf:
                # Store new record in database
                value = confs[key].get('default', '')
                stored_conf = self.configstore.put(key, util.serialize(value))

            else:
                # Get stored value
                value = util.deserialize(stored_conf.get_value())

            result[stored_conf.get_key()] = value

        return result

    def update_db(self, new_values):
        """ Update the configuration values stored in the database and the
            application's configuration using the given dictionary.

            The provided keys must be defined in the `WAFFLE_CONFS` setting.

            Params:

                new_values - dict of configuration variables and their values

                The dict has the following structure:

                    {
                        'MY_CONFIG_VAR'  : <CONFIG_VAL>,
                        'MY_CONFIG_VAR1' : <CONFIG_VAL1>
                    }

        """
        confs = self.app.config.get('WAFFLE_CONFS', {})
        to_update = {}

        for key in new_values.keys():
            # Some things cannot be changed...
            if key.startswith('WAFFLE_'):
                continue

            # No arbitrary keys
            if key not in confs.keys():
                continue

            value = new_values[key]
            updated = self.configstore.put(key, util.serialize(value))

            to_update[key] = value

        # Update config
        if not to_update:
            return

        self.app.config.update(to_update)

        # Notify other processes
        if self.app.config.get('WAFFLE_MULTIPROC', False) and _MULTIPROC:
            tstamp = time.time()
            self._tstamp = tstamp

            r = redis.client.StrictRedis()
            r.publish(self.app.config.get(
                'WAFFLE_REDIS_CHANNEL', 'waffleconf'), tstamp)


class WaffleConf(object):
    """ Initialize the Flask-WaffleConf extension

        Params:

            app         - Flask application instance
            configstore - WaffleStore instance
    """

    def __init__(self, app=None, configstore=None):
        if app and configstore:
            self.init_app(app, configstore)

    def init_app(self, app, configstore):
        """ Initialize the extension for the given application and store.

            Params:

                app         -- Flask application instance
                configstore -- WaffleStore instance

            Parse the configuration values stored in the database obtained from
            the WAFFLE_CONFS value of the configuration.
        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['waffleconf'] = _WaffleState(app, configstore)
