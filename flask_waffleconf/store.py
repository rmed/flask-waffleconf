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

#
# Based on flask_security.datastore module from Flask-Security by Matt Wright
#


class WaffleStore(object):
    """ Object for connecting to the application database. Offers common
        methods that have to be overriden depending on the database type / ORM
        used.

        Params:

            db    -- Database instance
            model -- Model to work with
    """

    def __init__(self, db=None, model=None):
        self.db = db
        self.model = model

    def commit(self):
        pass

    def delete(self, model, key):
        """ Remove a configuration variable from the database. """
        raise NotImplementedError

    def get(self, model, key):
        """ Obtain a configuration variable from the database. """
        raise NotImplementedError

    def put(self, model, key, value):
        """ Insert / Update a configuration variable in the database. """
        raise NotImplementedError


class PeeweeWaffleStore(WaffleStore):
    """ Config store for peewee. """

    def delete(self, key):
        record = self.get(self.model, key)

        if not record:
            return

        record.delete_instance()

    def get(self, key):
        try:
            return self.model.get(self.model.key == key)

        except self.model.DoesNotExist:
            # Does not exist
            return None

    def put(self, key, value):
        record = self.get(key)

        if not record:
            # Creating new record
            record = self.model()
            record.key = key

        record.value = value

        record.save()

        return record
