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

import os
import time

try:
    import redis
    _HAS_REDIS = True

except ImportError:
    _HAS_REDIS = False


def get_watcher(watcher_type):
    """Obtain a watcher function.

    These functions should be executed in a separate thread.

    Arguments:
        watcher_type (str): Either 'file' or 'redis'. If redis is not available,
            it will default to file watcher.

    Returns:
        Watcher function.
    """
    if watcher_type == 'redis' and _HAS_REDIS:
        return _redis_watcher

    else:
        return _file_watcher

def _file_watcher(state):
    """Watch for file changes and reload config when needed.

    Arguments:
        state (_WaffleState): Object that contains reference to app and its
            configstore.
    """
    conf = state.app.config

    file_path = conf.get('WAFFLE_WATCHER_FILE', '/tmp/waffleconf.txt')

    if not os.path.isfile(file_path):
        # Create watch file
        open(file_path, 'a').close()

    while True:
        tstamp = os.path.getmtime(file_path)

        # Compare timestamps and update config if needed
        if tstamp > state._tstamp:
            state.update_conf()
            state._tstamp = tstamp

        # Not too critical
        time.sleep(10)

def _redis_watcher(state):
    """Listen to redis channel for a configuration update notifications.

    Arguments:
        state (_WaffleState): Object that contains reference to app and its
            configstore.
    """
    conf = state.app.config

    r = redis.client.StrictRedis(
        host=conf.get('WAFFLE_REDIS_HOST', 'localhost'),
        port=conf.get('WAFFLE_REDIS_PORT', 6379))

    sub = r.pubsub(ignore_subscribe_messages=True)
    sub.subscribe(conf.get('WAFFLE_REDIS_CHANNEL', 'waffleconf'))

    while True:
        for msg in sub.listen():
            # Skip non-messages
            if not msg['type'] == 'message':
                continue

            tstamp = float(msg['data'])

            # Compare timestamps and update config if needed
            if tstamp > state._tstamp:
                state.update_conf()
                state._tstamp = tstamp

def get_notifier(notifier_type):
    """Obtain a notifier function.

    Arguments:
        notifier_type (str): Either 'file' or 'redis'. If redis is not available,
            it will default to file watcher.

    Returns:
        Notifier function.
    """
    if notifier_type == 'redis' and _HAS_REDIS:
        return _redis_notifier

    else:
        return _file_notifier

def _file_notifier(state):
    """Notify of configuration update through file.

    Arguments:
        state (_WaffleState): Object that contains reference to app and its
            configstore.
    """
    tstamp = time.time()
    state._tstamp = tstamp
    conf = state.app.config

    file_path = conf.get('WAFFLE_WATCHER_FILE', '/tmp/waffleconf.txt')

    if not os.path.isfile(file_path):
        # Create watch file
        open(file_path, 'a').close()

    # Update timestamp
    os.utime(file_path, (tstamp, tstamp))

def _redis_notifier(state):
    """Notify of configuration update through redis.

    Arguments:
        state (_WaffleState): Object that contains reference to app and its
            configstore.
    """
    tstamp = time.time()
    state._tstamp = tstamp
    conf = state.app.config

    # Notify timestamp
    r = redis.client.StrictRedis()
    r.publish(conf.get('WAFFLE_REDIS_CHANNEL', 'waffleconf'), tstamp)

def _dummy(state):
    """Does nothing."""
    pass
