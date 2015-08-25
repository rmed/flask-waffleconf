# Problem

The simple usage shown in the [Quickstart](quickstart.md) works fine when your
deployed application uses a single process (a single `app` instance). However,
chances are you are using something like
[uWSGI](https://uwsgi-docs.readthedocs.org/en/latest/), and your application
is served using several processes/workers.

If this is the case, when one of the workers (`app` instances) updates its
configuration values, the rest of the workers will still have their old
configuration values. If these old values are then updated, your application
workers will have inconsistent configuration variables all the way.

# Solution (kind of)

In **version 0.2.0**, `Flask-WaffleConf` introduced support for multiprocess
deployments by allowing these processes to listen and notify other processes
through a *Redis channel*.

While this means that you need to have Redis installed and running if you
intend to use this feature, it also means that workers will update their
configuration when another worker notifies them of an update in the values.

Currently, this can be done in two different ways:

- Using the [threading](https://docs.python.org/3/library/threading.html)
  module: the extension creates a thread for each application instance that
  will listen to the Redis channel and fetch the configuration from the
  database when notified.

- Using the [gevent](http://www.gevent.org/) module that employs *coroutines*
  and [greenlet](http://greenlet.readthedocs.org/en/latest/) for the same task.


While the first option is the simplest one, it also means that the application
will be under the influence of the
[GIL](https://wiki.python.org/moin/GlobalInterpreterLock). This should not be
much of an issue due to the listener blocking until a new message is received,
it may affect the performance of the application.

The second option should offer better performance because there is no need to
use the *GIL*, but may be more complex to configure depending on the
application server used.

# Setup for multiprocess use

First, you will need to install the `redis` and the `redis-py` module. For
Debian systems, this would be done like this:

~~~shell
# apt-get install redis-server

$ pip install redis
~~~

Now we need to set additional configuration variables in the application
configuration:

~~~python
# Enable multiprocess use
WAFFLE_MULTIPROC = True

# Redis host (defaults to 'localhost')
WAFFLE_REDIS_HOST = 'MY_HOST'

# Redis port (defaults to 6379)
WAFFLE_REDIS_PORT = 6379

# The channel to listen and send signals to (defaults to 'waffleconf')
WAFFLE_REDIS_CHANNEL = 'MY_CHANNEL'
~~~

Once the extension is initialized, the listener will be automatically created.

### Using threading

The `threading` module is used automatically if the `gevent` module is not
present.

You should check your server's documentation to see if you need to modify any
configuration in order to use threads in your application. For uWSGI, you would
need to use the `--enable-threads` option and use the `--lazy-apps` mode for
your application, due to the threads not working as intended in the *prefork*
model. For more information on this, check the [uWSGI
documentation](http://uwsgi-docs.readthedocs.org/en/latest/articles/TheArtOfGracefulReloading.html#preforking-vs-lazy-apps-vs-lazy).

### Using gevent

If the `gevent` module is installed, it will be imported first and use [monkey
patching](http://www.gevent.org/gevent.monkey.html) in order to use `greenlets`
instead of threads.

For uWSGI, you would need to enable `gevent` support as shown in [the
documentation](http://uwsgi-docs.readthedocs.org/en/latest/Gevent.html).
