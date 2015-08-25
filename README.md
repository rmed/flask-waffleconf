# Flask-WaffleConf [![PyPI version](https://img.shields.io/pypi/v/Flask-WaffleConf.svg)](https://pypi.python.org/pypi/Flask-WaffleConf)

A Flask extension that enables storage of configuration variables in the
database as well as runtime modification of these variables.

**Released under GPLv2+ license.**

# Installation

```shell
$ pip install Flask-WaffleConf
```

# Configuration

The extension uses the following configuration variables:

- `WAFFLE_CONFS`: Used for specifying the configuration variables that are
  going to be stored in the database. It has the following structure:

```python
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
```

- `WAFFLE_TEMPLATE`: Template containing the form used for updating the
  configuration values. You are highly encouraged to extend the default
  template.

- `WAFFLE_MULTIPROC`: Set it to `True` in order to enable multiprocess use
  (check [the
  documentation](https://flask-waffleconf.readthedocs.org/en/latest/multiproc/))

- `WAFFLE_REDIS_HOST`: Redis host to use for notifications.

- `WAFFLE_REDIS_PORT`: Port to use for the Redis connection.

- `WAFFLE_REDIS_CHANNEL`: Channel to use for the notifications.

# Example Application using peewee as ORM

```python
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
configstore = PeeweeWaffleStore(model=ConfModel)
waffle = WaffleConf(app, configstore)

# Plug the WaffleConf view to any of your Blueprints
register_waffle(app, 'waffleconf', '/config')
```

# Multiprocess deployments

Since **version 0.2.0**, multiprocess deployments are supported. Check [the
documentation](https://flask-waffleconf.readthedocs.org/en/latest/multiproc/)
for more information.

# Documentation

Documentation is present in the `docs/` directory and also online at
<https://flask-waffleconf.readthedocs.org>. In order to build the documentation
from source (you will need MkDocs), run:

```shell
$ mkdocs build
```
