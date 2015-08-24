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

def json_iter(obj):
    """ Create an iterator for a JSON object.

        Params:

            obj -- JSON object

        Returns:

            iterator
    """
    try:
        # Python 2.7.x
        return obj.viewitems()

    except:
        # Python 3.x
        return obj.items()

def parse_type(ctype, value):
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

    elif ctype == 'int':
        return int(value)

    elif ctype == 'float':
        return float(value)

    elif ctype == 'bool':
        if value == '0':
            return False
        else:
            return True
