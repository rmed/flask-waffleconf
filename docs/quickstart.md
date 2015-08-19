# Installation

**WaffleConf** only has *Flask* as a requirement. You can install the extension
by running:

~~~
$ pip install Flask-WaffleConf
~~~

# Configuration

The extension uses the following configuration variables:

- `WAFFLE_CONFS`: Used for specifying the configuration variables that are
  going to be stored in the database. It has the following structure:

~~~python
WAFFLE_CONFS = {
    'CONF_VAR1': {
        'type': 'str',
        'desc': 'First config var',
        'default': '0'
    },
    'CONF_VAR2': {
        'type': 'int',
        'desc': 'Second config var',
        'default': '0'
    }
}
~~~

- `WAFFLE_TEMPLATE`: Template containing the form used for updating the
  configuration values. You are highly encouraged to extend the default
  template.

# Example Application using peewee as ORM

~~~python
from flask import Flask
from flask.ext.waffleconf import WaffleConf, PeeweeWaffleStore, \
    WaffleMixin, register_waffle
import peewee

app = Flask(__name__)
app.config['WAFFLE_CONFS'] = {
    'CONF_VAR1': {
        'type': 'str',
        'desc': 'First config var',
        'default': '0'
    },
    'CONF_VAR2': {
        'type': 'int',
        'desc': 'Second config var',
        'default': '0'
    }
}

# Define your database
# db = ...

# Define model
class ConfModel(peewee.model, WaffleMixin):
    class Meta:
        database = db

    key = peewee.CharField(unique=True)
    value = peewee.TextField()

# Create database tables
# ...

# Initialize WaffleConf
configstore = PeeweeWaffleStore(ConfModel)
waffle = WaffleConf(app, configstore)

# Plug the WaffleConf view to any of your Blueprints
register_waffle(app, 'waffleconf', '/config')
~~~
