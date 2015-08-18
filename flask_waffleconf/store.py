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

            db -- Database instance
    """

    def __init__(self, db=None):
        self.db = None

    def commit(self):
        pass

    def delete(self, model):
        """ Remove a configuration variable from the database. """
        raise NotImplementedError

    def get(self, model, key):
        """ Obtain a configuration variable from the database. """
        raise NotImplementedError

    def put(self, model):
        """ Insert / Update a configuration variable in the database. """
        raise NotImplementedError


class MongoEngineWaffleStore(WaffleStore):
    """ Config store for MongoEngine. """

    def delete(self, model):
        model.delete()

    def get(self, model, key):
        pass

    def put(self, model):
        model.save()
        return model


class PeeweeWaffleStore(WaffleStore):
    """ Config store for peewee. """

    def delete(self, model):
        model.delete_instance()

    def get(self, model, key):
        try:
            return model.get(model.key == key)

        except model.DoesNotExist:
            # Does not exist
            return None

    def put(self, model):
        model.save()
        return model


class SQLAlchemyWaffleStore(WaffleStore):
    """ Config store for SQLAlchemy. """

    def commit(self):
        self.db.session.commit()

    def delete(self, model):
        self.db.session.delete(model)

    def get(self, model, key):
        pass

    def put(self, model):
        self.db.session.add(model)
        return model
