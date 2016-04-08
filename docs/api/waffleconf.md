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

**Changed in `0.3.0`**: the extension no longer exposes views or templates.
Instead, the developer should call the methods of this object from their
(secured) views.

### Initialization

##### ***_WaffleState(app, configstore)***

Initializes the object. Once initialized, it parses the configuration in the
database, updating the keys in `app.config` where needed.

### Methods

#### ***_listen_updates()***

Method that initializes the listener when `WAFFLE_MULTIPROC` is set to `True`.
The listener awaits messages from Redis, checks the *timestamp* of the message
and if it is greater than the one stored, updates the application configuration
and the timestamp.

---

#### ***parse_conf(keys=[])***

Parse the configuration keys specified.

##### Parameters

- `keys`: `list` of keys to parse. If the list is empty, all the keys known to
  the application will be used

##### Returns

- `dict`: parsed configuration values with their proper data types using the
  configuration variable id as key

---

#### ***update_db(new_values)***

Update configuration variables stored in the database. This also updates the
application configuration.

When `WAFFLE_MULTIPROC` is set to `True`, this method will also notify the
update to the other application instances.

##### Parameters

- `new_values`: `dict` of updated configuration variables and their values

The dict has the following structure:

```python
{
    'MY_CONFIG_VAR'  : <CONFIG_VAL>,
    'MY_CONFIG_VAR1' : <CONFIG_VAL1>
}
```

This dictionary does not have to include all the keys available, and may be
used to only update some of the variables.
