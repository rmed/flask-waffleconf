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
from flask import current_app, render_template, request
from flask.views import MethodView
from .util import json_iter, parse_type


class WaffleView(MethodView):
    """ View for displaying WaffleConf configuration variables in a form
        and update the variables when performing a POST request.
    """

    def get(self):
        """ Display a form with all the configuration variables defined in
            WAFFLE_CONFS.
        """
        app = current_app
        app_conf = app.config
        state = app.extensions['waffleconf']

        configs = []

        iterator = json_iter(app_conf['WAFFLE_CONFS'])

        for key, conf in iterator:
            new_el = {
                'key'   : key,
                'type'  : conf['type'],
                'desc'  : conf['desc']
            }

            if new_el['type'] == 'str':
                new_el['value'] = app_conf[key]

            elif new_el['type'] == 'json':
                new_el['value'] = json.dumps(app_conf[key])

            else:
                new_el['value'] = str(app_conf[key])

            configs.append(new_el)

        return render_template(state.form_template, configs=configs)

    def post(self):
        """ Update the values that have been modified and update the application
            configuration.
        """
        app = current_app
        state = app.extensions['waffleconf']
        wconfs = app.config['WAFFLE_CONFS']

        form = request.form
        to_update = {}

        iterator = json_iter(form)

        for key, value in iterator:
            updated = parse_type(wconfs[key]['type'], value)

            if updated != app.config[key]:
                to_update[key] = value

        # Perform update
        state.update_conf(to_update)

        return self.get()


def register_waffle(blueprint, endpoint, url, decorators=[]):
    """ Register the WaffleView in the given blueprint.

        Params:

            blueprint   -- blueprint to register the view in
            endpoint    -- endpoint for the view
            url         -- url for accessing the view
            decorators  -- list of decorator functions to apply to the view
    """
    view = WaffleView()
    view_func = view.as_view(endpoint)

    # Apply decorators
    for deco in decorators:
        view_func = deco(view_func)

    # Register rule
    blueprint.add_url_rule(url, view_func=view_func, methods=['GET', 'POST'])
