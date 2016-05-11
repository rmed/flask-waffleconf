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

import base64
import pickle

def deserialize(data):
    """Deserialize data using base64 encoding and pickle.

    Arguments:
        data (str): Data to deserialize (must be in base64 and pickled)

    Returns:
        Unpickled object.
    """
    return pickle.loads(base64.b64decode(data.encode()))

def serialize(data):
    """Serialize data using pickle and converting it to a base64 string.

    Arguments:
        data: data to serialize (must be picklable)

    Returns:
        Serialized object.
    """
    return base64.b64encode(pickle.dumps(data)).decode('utf-8')
