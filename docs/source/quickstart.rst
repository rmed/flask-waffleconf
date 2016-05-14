Quickstart
==========

Installation
------------

**WaffleConf** only has *Flask* as a *hard* requirement. You can install the
extension by running::

    pip install Flask-WaffleConf

Configuration
-------------

Simple usage of the extension requires the following configuration variables
(e.g., in your application's ``config.py``):

* ``WAFFLE_CONFS``: used for specifying the configuration variables that are
    going to be stored in the database. It has the following structure:

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

For more detailed information, check :doc:`configuration`.

Example Application using SQLAlchemy as ORM
-------------------------------------------

.. code-block:: python

	from flask import Flask, current_app
	from flask_waffleconf import WaffleConf, AlchemyWaffleStore, \
		WaffleMixin
	from flask_sqlalchemy import SQLAlchemy

	app = Flask(__name__)
	app.config['WAFFLE_CONFS'] = {
		'MAX_FILESIZE': {
			'desc': 'Max upload filesize (in bytes)',
			'default': 1000
		},

		'SITENAME': {
			'desc': 'Name of the site appearing in the header',
			'default': 'Waffle'
		}
	}

	# Define your database
	# db = ...

	# Define model
	class ConfModel(db.Model, WaffleMixin):
        __tablename__ = 'confs'

        id = db.Column(db.Integer, primary_key=True)
		key = db.Column(db.String(255), unique=True)
		value = db.Column(db.Text)

	# Create database tables
	# ...

	# Initialize WaffleConf
	configstore = AlchemyWaffleStore(db=db, model=ConfModel)
	waffle = WaffleConf(app, configstore)

	@app.route('/')
	def index():
		"""Display content of configured variable 'SITENAME'."""
		state = current_app.extensions['waffleconf']

		parsed = state.parse_conf()
		# {'MAX_FILESIZE': 1000, 'SITENAME': 'Waffle'}

		return parsed['SITENAME']

Example Application using peewee as ORM
---------------------------------------

.. code-block:: python

	from flask import Flask, current_app
	from flask_waffleconf import WaffleConf, PeeweeWaffleStore, \
		WaffleMixin
	import peewee

	app = Flask(__name__)
	app.config['WAFFLE_CONFS'] = {
		'MAX_FILESIZE': {
			'desc': 'Max upload filesize (in bytes)',
			'default': 1000
		},

		'SITENAME': {
			'desc': 'Name of the site appearing in the header',
			'default': 'Waffle'
		}
	}

	# Define your database
	# db = ...

	# Define model
	class ConfModel(peewee.Model, WaffleMixin):
		class Meta:
			database = db

		key = peewee.CharField(unique=True)
		value = peewee.TextField()

	# Create database tables
	# ...

	# Initialize WaffleConf
	configstore = PeeweeWaffleStore(model=ConfModel)
	waffle = WaffleConf(app, configstore)

	@app.route('/')
	def index():
		"""Display content of configured variable 'SITENAME'."""
		state = current_app.extensions['waffleconf']

		parsed = state.parse_conf()
		# {'MAX_FILESIZE': 1000, 'SITENAME': 'Waffle'}

		return parsed['SITENAME']
