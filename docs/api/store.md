# Configuration store

In order to adapt to different ORM or database connectors, WaffleConf uses
a *configuration store*. The store exposes methods `get()`, `put()`, `delete()`
and `commit()` (when needed). Stores are very easy to use:

~~~python
from flask.ext.waffleconf import PeeweeWaffleStore

# mymodel = ...

store = PeeweeWaffleStore(model=mymodel)
~~~

**Version 0.1.0 only has defined peewee support. More stores will be added in
the future. Until then, you can subclass the `WaffleStore` class to define
your own store. This can be done as follows:**

~~~python
from flask.ext.waffleconf import WaffleStore

class MyStore(WaffleStore):

    def commit(self):
        # Do a commit

    def delete(self, key):
        # Delete a configuration

    def get(self, key):
        # Get a configuration

    def put(self, key, value):
        # Insert/Update a configuration
~~~

Note that, by default, you can pass a database instance `db` and a model
instance `model` to the `WaffleStore` class.

### Methods

#### ***commit()***

Perform a commit in the database. This is needed in connectors such as
SQLAlchemy.

---

#### ***delete(key)***

Delete a configuration variable from the database.

##### Parameters

- `key`: unique identifier of the variable to delete.

---

#### ***get(key)***

Obtain the specified **record** from the database.

##### Parameters

- `key`: unique identifier of the variable to obtain.

##### Returns

- `WaffleMixin`

---

#### ***put(key, value)***

Insert a value into the given configuration id.

##### Parameters

- `key`: unique identifier of the variable to modify.
- `value`: string representation of the value to insert.

##### Returns

- `WaffleMixin`
