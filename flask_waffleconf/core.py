# -*- coding: utf-8 -*-
#
# Flask-WaffleConf - https://github.com/rmed/flask-waffleconf
#
# Copyright (C) 2015  Rafael Medina García <rafamedgar@gmail.com>
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

from flask import Blueprint
from .util import json_iter, parse_type
import time
import redis
import threading


class _WaffleState(object):
    """ Store configstore for the app state.

        Params:

            app         -- Flask application instance
            configstore -- WaffleStore instance

        This object will update its application configuration and if the
        `WAFFLE_MULTIPROC` setting is set to True, it will also notify other
        processes using Redis.
    """

    def __init__(self, app, configstore):
        self.app = app
        self.configstore = configstore

        if self.app.config.get('WAFFLE_MULTIPROC', False):
            # Multiprocess update notification
            self._tstamp = time.time()

            self._listener = threading.Thread(target=self._listen)
            self._listener.setDaemon(True)
            self._listener.start()

        self.form_template = self.app.config.get(
            'WAFFLE_TEMPLATE', 'waffleconf/waffle_form.html')

        configs = self.app.config.get('WAFFLE_CONFS', {})

        if not configs:
            return None

        parsed = self._parse_conf(configs)

        # Update app config
        self.app.config.update(parsed)

    def _listen(self):
        """ Listen in redis for a configuration update notification. """
        r = redis.client.StrictRedis()
        sub = r.pubsub()
        sub.subscribe('waffleconf')

        while True:
            for msg in sub.listen():
                # Skip non-messages
                if not msg['type'] == 'message':
                    continue

                tstamp = float(msg['data'])
                print('--------------RECEIVING-------------')
                print(msg)
                print(tstamp, self._tstamp)
                # Compare timestamps and update config if needed
                if tstamp > self._tstamp:
                    configs = self.app.config.get('WAFFLE_CONFS', {})
                    parsed = self._parse_conf(configs)

                    self.app.config.update(parsed)
                    self._tstamp = tstamp

    def _parse_conf(self, configs):
        """ Parse configuration values from the database specified in the
            `configs` argument. The extension must have been previously
            initialized!

            Params:

                configs -- dict of configuration variables (dicts)

                The dicts have the following structure:

                    {
                        'key'     : 'MY_CONFIG_VAR',
                        'type'    : <TYPE OF THE VAR>,
                        'desc'    : <TEXT DESCRIPTION OF THE VAR>,
                        'default' : <DEFAULT VALUE>
                    }

            If a key is not found in the database, itwill be created with the
            default value specified.

            Returns:

                result -- dict of the parsed config values
        """
        result = {}

        iterator = json_iter(configs)

        for key, conf in iterator:
            db_conf = self.configstore.get(key)

            if not db_conf:
                # Create variable in database
                db_conf = self.configstore.put(key, conf['default'])

            result[db_conf.get_key()] = parse_type(
                conf['type'], db_conf.get_value())

        return result

    def update_conf(self, configs):
        """ Update configuration variables in the database. This also updates
            the application configuration.

            Params:

                configs -- dict of configuration variables and their values

                The dict has the following structure:

                    {
                        'MY_CONFIG_VAR'  : 'CONFIG_VAL',
                        'MY_CONFIG_VAR1' : 'CONFIG_VAL1'
                    }

        """
        result = {}

        iterator = json_iter(configs)

        for key, value in iterator:
            updated = self.configstore.put(key, value)

            result[key] = parse_type(
                self.app.config['WAFFLE_CONFS'][key]['type'], updated.value)

        self.app.config.update(result)

        # Notify other processes
        if self.app.config.get('WAFFLE_MULTIPROC', False):
            print('-------------NOTIFYING----------')
            tstamp = time.time()
            print(tstamp)
            self._tstamp = tstamp

            r = redis.client.StrictRedis()
            r.publish('waffleconf', tstamp)


class WaffleConf(object):
    """ Initialize the Flask-WaffleConf extension

        Params:

            app         -- Flask application instance
            configstore -- WaffleStore instance
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

        module = Blueprint(
            'waffleconf',
            __name__,
            template_folder='templates')

        app.register_blueprint(module)
