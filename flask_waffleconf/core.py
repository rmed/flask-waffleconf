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

from __future__ import absolute_import

from . import util
from . import watcher
import threading
import time


class _WaffleState(object):
    """Store configstore for the app state.

    This object will update its application's configuration and if the
    ``WAFFLE_MULTIPROC`` setting is set to True, it will also notify other
    processes using Redis channel or file timestamp.

    Arguments:
        app: Flask application instance.
        configstore (WaffleStore): database store.
    """

    def __init__(self, app, configstore):
        self.app = app
        self.configstore = configstore

        # Setup multiprocess notifications
        if self.app.config.get('WAFFLE_MULTIPROC', False):
            op_type = self.app.config.get('WAFFLE_WATCHTYPE', 'file')

            self.watch = watcher.get_watcher(op_type)
            self.notify = watcher.get_notifier(op_type)

            self._tstamp = time.time()

            self._watcher = threading.Thread(target=self.watch, args=(self,))
            self._watcher.setDaemon(True)
            self._watcher.start()

        # Get configs from database
        self.update_conf()

    def parse_conf(self, keys=[]):
        """Parse configuration values from the database.

        The extension must have been previously initialized.

        If a key is not found in the database, it will be created with the
        default value specified.

        Arguments:
            keys (list[str]): list of keys to parse. If the list is empty, then
                all the keys known to the application will be used.

        Returns:
            dict of the parsed config values.
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
                self.configstore.commit()

            else:
                # Get stored value
                value = util.deserialize(stored_conf.get_value())

            result[stored_conf.get_key()] = value

        return result

    def update_db(self, new_values):
        """Update database values and application configuration.

        The provided keys must be defined in the ``WAFFLE_CONFS`` setting.

        Arguments:
            new_values (dict): dict of configuration variables and their values
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
            self.configstore.put(key, util.serialize(value))
            self.configstore.commit()

            to_update[key] = value

        # Update config
        if not to_update:
            return

        self.app.config.update(to_update)

        # Notify other processes
        if self.app.config.get('WAFFLE_MULTIPROC', False):
            self.notify(self)

    def update_conf(self):
        """Update configuration values from database.

        This method should be called when there is an update notification.
        """
        parsed = self.parse_conf()

        if not parsed:
            return None

        # Update app config
        self.app.config.update(parsed)


class WaffleConf(object):
    """Initialize the Flask-WaffleConf extension

    Arguments:
        app: Flask application instance
        configstore (WaffleStore): database store.
    """

    def __init__(self, app=None, configstore=None):
        if app and configstore:
            self.init_app(app, configstore)

    def init_app(self, app, configstore):
        """Initialize the extension for the given application and store.

        Parse the configuration values stored in the database obtained from
        the ``WAFFLE_CONFS`` value of the configuration.

        Arguments:
            app: Flask application instance
            configstore (WaffleStore): database store.

        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}

        app.extensions['waffleconf'] = _WaffleState(app, configstore)
