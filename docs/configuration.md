# `WAFFLE_CONFS`

The `WAFFLE_CONFS` variable is used to specify information on each of the
variables that are going to be stored in the database:

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

- `type`: specifies the data type of the variable. Available types are:

    - Boolean   ~> bool
    - Float     ~> float
    - Integer   ~> int
    - JSON      ~> json
    - Strings   ~> str

- `desc`: human-readable name or short description of the variable
- `default`: default value when the variable does not exist in the database.
  **Should be a string**

---

# `WAFFLE_TEMPLATE`

The extension only uses a single template that contains a form for displaying
and updating the values.

**You are highly encouraged to extend this template.**

Defaults to `'waffleconf/waffle_form'`.

---

# `WAFFLE_MULTIPROC`

Set it to `True` in order to enable the extension for multiprocess deployments
(see [Multiprocess deployments](multiproc.md)) for more information.

Defaults to `False`.

---

# `WAFFLE_REDIS_HOST`

The Redis host to use for sending update notifications to other application
instances.

Defaults to `'localhost'`.

---

# `WAFFLE_REDIS_PORT`

The port to use in order to connect to Redis.

Defaults to `6379`.

---

# `WAFFLE_REDIS_CHANNEL`

The channel to use for application instance communication (sending and
receiving update notifications).

Defaults to `'waffleconf'`.
