Multiprocess deployments
========================

.. _uWSGI: https://uwsgi-docs.readthedocs.org/en/latest/
.. _GIL: https://wiki.python.org/moin/GlobalInterpreterLock

Problem
-------

The simple usage shown in the :doc:`quickstart` works fine when your deployed
application uses a single process (i.e., a single app instance). However,
chances are you are using something like uWSGI_, and your application is served
using several processes/workers.

If this is the case, when one of the workers (``app`` instances) updates its
configuration values, the rest of the workers will still have their old
configuration values. If these old values are then updated, your application
workers will have inconsistent configuration variables all the way.

Solution (kind of)
------------------

In *version 0.2.0*, ``Flask-WaffleConf`` introduced support for multprocess
deployments by allowing these processes to listen for and send updates through
a *Redis channel*.

*Version 0.3.0* introduced a simpler approach by using *stat* information from
a plain file in the filesystem.

The mode to use can be configured setting the value of the ``WAFFLE_WATCHTYPE``
variable (see :doc:`configuration`).

.. note::
    As both approaches use threads, the GIL_ should be taken into account,
    although it should not be much of an issue performance-wise.

.. note::
    Application servers (such as uWSGI_) may require additional configuration
    to enable threads in hosted applications. For uWSGI, for instance, the
    ``--enable-threads`` and ``--lazy-apps`` flags are needed.

Setup for multiprocess deployments
----------------------------------

*Changed in version 0.3.0*: ``gevent`` support was removed as the
implementation was not correct.

File watching
~~~~~~~~~~~~~

Using a file is the simplest approach for notifications and does not require
any additional dependencies. Simply set ``WAFFLE_WATCHTYPE`` to ``'file'`` and
change the ``WAFFLE_WATCHER_FILE`` to a valid filesystem path. If it does not
exist, it will be created automatically.

*Added in version 0.3.0*.

Redis pub/sub
~~~~~~~~~~~~~

Using Redis for notifications requires a valid connection to a Redis server
(usually in localhost), as well as the ``redis-py`` module. Local installation
in Debian systes would be done like this::

   apt-get install redis-server

   pip install redis

Next, it is necessary to set additional configuration variables in the
configuration of the application:

.. code-block:: python

    # Enable multiprocess use
    WAFFLE_MULTIPROC = True

    # Redis host (defaults to 'localhost')
    WAFFLE_REDIS_HOST = 'MY_HOST'

    # Redis port (defaults to 6379)
    WAFFLE_REDIS_PORT = 6379

    # The channel to listen and send signals to (defaults to 'waffleconf')
    WAFFLE_REDIS_CHANNEL = 'MY_CHANNEL'

Once the extension is initialized, the listener will be automatically created.

.. note::
    Configuring the extension to use Redis without the ``redis-py`` module
    installed will fallback to the default *file watcher* configuration.
