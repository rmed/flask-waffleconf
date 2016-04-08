# Model

WaffleConf expects a database model that has a `key` and a `value` attribute,
where `key` must/should be unique. The `WaffleMixin` object can be used to
instantiate the model, as it exposes the `get_key()` and `get_value()` methods
necessary for obtaining the data in a generic way.

```python
# Using peewee as example
import peewee
from flask_waffleconf import WaffleMixin

class ConfModel(peewee.Model, WaffleMixin)
    key = peewee.CharField(unique=True)
    value = peewee.TextField()
```

These two methods simply return `self.key` and `self.value`, so you can
**override** them and adapt them accordingly.
