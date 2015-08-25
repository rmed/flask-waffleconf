# WaffleConf

The `WaffleConf` object initializes the application state for performing
configuration udpates.

Notice that every time there is a change in the values for the variables
defined in `WAFFLE_CONFS`, the database values and those in `app.config` will
be refreshed.

### Initialization

#### ***WaffleConf(app=None, configstore=None)***

Calls the `init_app()` method with the given `app` and `configstore`
parameters.

##### Parameters

- `app`: Flask application instance
- `configstore`: `WaffleStore` instance

### Methods

#### ***init_app(app, configstore)***

Initializes the state object and registers the `waffleconf` blueprint for
accessing the default template.


# _WaffleState

This is the object stored in `app.extensions['waffleconf']`, and is in charge
of performing the parsing and updating of the configuration variables.

In addition, it stores the form template to use in order to display/update the
configuration variables. If the `WAFFLE_TEMPLATE` variable is not set in the
configuration, it will default to `waffleconf/waffle_form.html`.

### Initialization

##### ***_WaffleState(app, configstore)***

Initializes the object. Once initialized, it parses the configuration in the
database, updating the keys in `app.config` where needed.

### Methods

#### ***_listen()***

Method that initializes the listener when `WAFFLE_MULTIPROC` is set to `True`.
The listener awaits messages from Redis, checks the *timestamp* of the message
and if it is greater than the one stored, updates the application configuration
and the timestamp.

---

#### ***_parse_conf(configs)***

Parse the configuration in the database and store the values in `app.config`.

##### Parameters

- `configs`: `dict` obtained from `app.config['WAFFLE_CONFS']` which contains
  information on each variable.

##### Returns

- `dict`: parsed configuration values with their proper data types using the
  configuration variable id as key.

---

#### ***update_conf(configs)***

Update configuration variables in the database. This also updates the
application configuration.

When `WAFFLE_MULTIPROC` is set to `True`, this will also notify the update to
the other application instances.

##### Parameters

- `configs`: `dict` of configuration variables and their values

The dict has the following structure:

~~~python
{
    'MY_CONFIG_VAR'  : 'CONFIG_VAL',
    'MY_CONFIG_VAR1' : 'CONFIG_VAL1'
}
~~~

Ideally, this dict is obtained from a form.
