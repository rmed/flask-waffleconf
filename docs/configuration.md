# `WAFFLE_CONFS`

The `WAFFLE_CONFS` variable is used to specify information on each of the
variables that are going to be stored in the database:

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

- `desc`: human-readable name or short description of the variable
- `default`: default value when the variable does not exist in the database.
  **Should be a string**

**Changed in `0.3.0`**: the `type` field is deprecated as values are serialized
when stored in the database and deserialized when obtained with `parse_conf()`.

---

# `WAFFLE_TEMPLATE`

**Changed in `0.3.0`**: the `WAFFLE_TEMPLATE` setting is deprecated, as the
extension is now implemented to be called from user-created views.

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
