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


class WaffleMixin(object):
    """Mixin used in the creation of the database model.

    WaffleConf expects a model that has (at least) the following fields:

        - key (str): Unique identifier for configuration variable.
        - value (str): Value for the configuration variable.

    Values may be a large string, so make sure to define a field capable
    of storing big strings. These values are later parsed according to the
    ``type`` specified in the application configuration.
    """

    def get_key(self):
        """Obtain the key for the configuration variable.

        Mixin expects a ``self.key`` attribute (str) in the model.
        If this is not the case, you should override this method.

        Returns:
            Configuration key string.
        """
        try:
            return self.key

        except AttributeError:
            raise NotImplementedError("Model does not have attribute 'key'")

    def get_value(self):
        """Obtain the value for the configuration variable.

        Mixin expects a ``self.value`` attribute (str) in the model.
        If this is not the case, you should override this method.

        Returns:
            Configuration value string.
        """
        try:
            return self.value

        except AttributeError:
            raise NotImplementedError("Model does not have attribute 'value'")
