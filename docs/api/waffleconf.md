# WaffleConf

The `WaffleConf` object stores the previously defined `WaffleStore` and the
application in order to access its configuration for updates.

Notice that every time there is a change in the values for the variables
defined in `WAFFLE_CONFS`, the database values and those in `app.config` will
be refreshed.

### Initialization

#### ***WaffleConf(app=None, configstore=None)***

Initializes the object with the given `app` and `configstore` and calls the
`init_app()` method.

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

#### ***_parse_conf(configs)***

Parse the configuration in the database and store the values in `app.config`.
This method is only called on startup.

##### Parameters

- `configs`: `dict` obtained from `app.config['WAFFLE_CONFS']` which contains
  information on each variable.

##### Returns

- `dict`: parsed configuration values with their proper data types using the
  configuration variable id as key.

---

#### ***_parse_type(ctype, value)***

Parse the configuration according to the type specified.

##### Parameters

- `ctype`: string identifying the data type of the variable. Available types:

    - Boolean   ~> bool
    - Float     ~> float
    - Integer   ~> int
    - JSON      ~> json
    - Strings   ~> str

- `value`: string representation of the value to parse.

##### Returns

Parsed result

---

#### ***update_conf(configs)***

Update configuration variables in the database. This also updates the
application configuration.

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
