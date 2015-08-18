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


class WaffleView(MethodView):
    """ View for displaying WaffleConf configuration variables in a form
        and update the variables when performing a POST request.

        Params:

            wconf -- instantiated WaffleConf object
    """

    def get(self):
        app = current_app
        app_conf = app.config
        state = app.extensions['waffleconf']

        configs = []

        try:
            # Python 2.7.x
            iterator = app_conf['WAFFLE_CONFS'].viewitems()

        except:
            # Python 3.x
            iterator = app_conf['WAFFLE_CONFS'].items()

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
        app = current_app
        state = app.extensions['waffleconf']
        wconfs = app.config['WAFFLE_CONFS']

        form = request.form
        to_update = {}

        try:
            # Python 2.7.x
            iterator = form.viewitems()

        except:
            # Python 3.x
            iterator = form.items()

        for key, value in iterator:
            updated = state._parse_type(
                wconfs[key]['type'], value)

            if updated != app.config[key]:
                to_update[key] = value

        # Perform update
        state.update_conf(to_update)

        return self.get()

def register_waffle(blueprint, endpoint, url, decorators=[]):
    """ Register the WaffleView in the given blueprint.

        Params:

            wconf       -- instantiated WaffleConf object
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
