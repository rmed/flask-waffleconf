# Installation

**WaffleConf** only has *Flask* as a requirement. You can install the extension
by running:

```
$ pip install Flask-WaffleConf
```

# Configuration

Simple usage of the extension requires the following configuration variables:

- `WAFFLE_CONFS`: Used for specifying the configuration variables that are
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

# Example Application using peewee as ORM

```python
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
    """ Display all the configuration variables ."""
    state = current_app.extensions['waffleconf']

    parsed = state.parse_conf()
    # {'MAX_FILESIZE': 1000, 'SITENAME': 'Waffle'}

    return parsed['SITENAME']
```
