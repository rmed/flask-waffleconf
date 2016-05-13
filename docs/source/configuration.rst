Configuration
=============

The extension relies on several configuration variables that should be present
in the ``config`` dict from the Flask application it is attached to.


WAFFLE_CONFS
------------

The ``WAFFLE_CONFS`` variable is used to specify information on each of the
variables that are going to be stored in the database:

.. code-block:: python

   WAFFLE_CONFS = {
		'MAX_FILESIZE': {
			'desc': 'Max upload filesize (in bytes)',
			'default': 1000
		},

		'SITENAME': {
			'desc': 'Name of the site appearing in the header',
			'default': 'Waffle'
		}
	}

It is a simple ``dict`` that uses the name of the configuration variable to
store as key and stores child ``dict`` objects with the following attributes:

- ``desc``: human-readable name or short description of the variable
- ``default``: default value when the variable does not exist in database
    (**Must be picklable**)

.. note::
    Only variables that appear in this dict can be updated during runtime.

*Changed in 0.3.0*: the ``type`` field is deprecated as values are serialized
when stored in the database and deserialized when obtained with
:py:meth:`~flask_waffleconf.core._WaffleState.parse_conf`.

WAFFLE_MULTIPROC
----------------

When set to ``True``, the extension will take into account multiprocess
deployments. See :doc:`multiproc` for more information.

Defaults to ``False``.

WAFFLE_WATCHTYPE
----------------

Specifies the medium that will be used to notify other application instances
when there is a change in the variables stored in database. Supported values
are:

- ``'file'``: use timestamps of a plain file in the filesystem (default)
- ``'redis'``: use a Redis channel with pub/sub

*Added in version 0.3.0*.

WAFFLE_WATCHER_FILE
-------------------

Path to the file to use when using a file watcher to check for updates. This
file is polled every *10 seconds* in a separate thread and its timestamp
checked against the one stored in the
:py:class:`~flask_waffleconf.core._WaffleState` object instance.

Defaults to ``'/tmp/waffleconf.txt'``.

.. warning::
    Make sure that the user running the application has the necessary
    permissions to check and update the timestamp of the file.

*Added in version 0.3.0*.

WAFFLE_REDIS_HOST
-----------------

When using Redis for update notifications, this variable is used to determine
the host to be used in the connection.

Defaults to ``'localhost'``.

WAFFLE_REDIS_PORT
-----------------

When using Redis for update notifications, this variable is used to determine
the port to be used in the connection.

Defaults to ``6379``.

WAFFLE_REDIS_CHANNEL
--------------------

When using Redis for update notifications, this variable is used to determine
the channel to be used for the pub/sub messages.

Defaults to ``'waffleconf'``.


Deprecated
----------

The following variables are deprecated in the latest version of the
extension.

WAFFLE_TEMPLATE
~~~~~~~~~~~~~~~

*Deprecated in version 0.3.0: the extension no longer uses any views or
templates.*

The extension only uses a single template that contains a form for displaying
and updating the values.

**You are highly encouraged to extend this template.**

Defaults to ``'waffleconf/waffle_form'``.
