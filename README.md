# Flask-WaffleConf [![PyPI version](https://img.shields.io/pypi/v/Flask-WaffleConf.svg)](https://pypi.python.org/pypi/Flask-WaffleConf)

WaffleConf is a Flask extension that enables storage of configuration variables
in the database as well as runtime modification of said variables.

**Released under GPLv2+ license.**

# Installation

```shell
$ pip install Flask-WaffleConf
```

# Configuration

Simple usage of the extension requires the following configuration variables
(e.g., in your application's `config.py`):

- `WAFFLE_CONFS`: used for specifying the configuration variables that are
    going to be stored in the database. It has the following structure:

```python
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
```

Check the
[documentation](https://flask-waffleconf.readthedocs.org/en/latest/multiproc/)
for advanced usage

# Example Application using SQLAlchemy as ORM

```python
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

@app.before_first_request
def do_before():
    """Update stored configurations."""
    waffle.state.update_conf()

@app.route('/')
def index():
    """Display content of configured variable 'SITENAME'."""
    state = current_app.extensions['waffleconf']

    parsed = state.parse_conf()
    # {'MAX_FILESIZE': 1000, 'SITENAME': 'Waffle'}

    return parsed['SITENAME']
```

# Multiprocess deployments

Since **version 0.2.0**, multiprocess deployments are supported. Check [the
documentation](https://flask-waffleconf.readthedocs.org/en/latest/multiproc/)
for more information.

# Documentation

Documentation is present in the `docs/` directory and also online at
<https://flask-waffleconf.readthedocs.org>. In order to build the documentation
from source (you will need Sphinx), run the following command in the `docs/`
directory:

```shell
$ make html
```
