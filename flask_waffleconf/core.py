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

import json
from flask import Blueprint
from .util import json_iter


class _WaffleState(object):
    """ Store configstore and model for the app state.

        Params:

            app         -- Flask application instance
            configstore -- WaffleStore instance
            model       -- Model that stores the variables in database
    """

    def __init__(self, app, configstore, model):
        self.app = app
        self.configstore = configstore
        self.model = model

        self.form_template = self.app.config.get(
            'WAFFLE_TEMPLATE', 'waffleconf/waffle_form.html')

        configs = self.app.config.get('WAFFLE_CONFS', None)

        if not configs:
            return None

        parsed = self._parse_conf(configs)

        # Update app config
        self.app.config.update(parsed)

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
            db_conf = self.configstore.get(self.model, key)

            if not db_conf:
                # Create variable in database
                db_conf = self.configstore.put(
                    self.model, key, conf['default'])

            result[db_conf.get_key()] = self._parse_type(
                conf['type'], db_conf.get_value())

        return result

    def _parse_type(self, ctype, value):
        """ Parse the configuration according to the type specified.

            Available types:

                - Boolean   ~> bool
                - Float     ~> float
                - Integer   ~> int
                - JSON      ~> json
                - Strings   ~> str

            Params:

                ctype  -- type to parse
                value  -- configuration value obtained from the database

            Returns:

                parsed -- parsed result
        """
        if ctype == 'str':
            # Default type
            return value

        elif ctype == 'json':
            try:
                return json.loads(value)

            except ValueError:
                # Malformed json?
                return None


    def update_conf(self, configs):
        """ Update configuration variables in the database. This also updates
            the application configuration.

            Params:

                configs -- dict configuration variables

                The dicts have the following structure:

                    {
                        'MY_CONFIG_VAR'  : 'CONFIG_VAL',
                        'MY_CONFIG_VAR1' : 'CONFIG_VAL1'
                    }

        """
        result = {}

        iterator = json_iter(configs)

        for key, value in iterator:
            updated = self.configstore.put(self.model, key, value)

            result[key] = self._parse_type(
                self.app.config['WAFFLE_CONFS'][key]['type'], updated.value)

        self.app.config.update(result)

class WaffleConf(object):
    """ Initialize the Flask-WaffleConf extension

        Params:

            app         -- Flask application instance
            configstore -- WaffleStore instance
            model       -- Model that stores the variables in database
    """

    def __init__(self, app=None, configstore=None, model=None):
        self.app = app
        self.configstore = configstore
        self.model = model

        if app and configstore and model:
            self.init_app(app, configstore)

    def init_app(self, app, configstore):
        """ Initialize the extension for the given application and store.

            Params:

                app         -- Flask application instance
                configstore -- WaffleStore instance

            Parse the configuration values stored in the database obtained from
            the WAFFLE_CONFS value of the configuration.
        """
        if not hasattr(self.app, 'extensions'):
            app.extensions = {}

        self.app.extensions['waffleconf'] = _WaffleState(
            self.app, self.configstore, self.model)

        module = Blueprint(
            'waffleconf',
            __name__,
            template_folder='templates')

        app.register_blueprint(module)
