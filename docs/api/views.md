# WaffleView

The `WaffleView` class is a *plugabble view* that exposes `GET`  and `POST`
routes for viewing and updating the configuration variables.

### Methods

#### ***get()***

Displays a form with all the configuration variables specified in
`WAFFLE_CONFS`.

The form receives a `list` of `dicts` in the parameter `configs` containing:

- `key`:  unique identifier of the variable
- `type`: type of the variable
- `desc`: human-readable name or description of the variable
- `value`: string representation of the variable (for the input fields)

---

#### ***post()***

Updates the values that have been modified and refreshes the application
configuration.

Once this process is done, redirects to the `get()` view, displaying the new
values.

# Plugging the view

Given the structure of `WaffleView`, it is possible to *plug* it into any of
the Blueprints present in your application (or even to the application itself).
This is done through the `register_waffle()` function.

---

#### ***register_waffle(blueprint, endpoint, url, decorators=[])***

Register the `WaffleView` in the given blueprint.

##### Parameters

- `blueprint`: Blueprint to register the view in
- `endpoint`: endpoint for the view
- `url`: url for accessing the view
- `decorators`: list of decorator functions to apply to the view

---

A practical example of this would be having an `admin` Blueprint that is
secured by `Flask-Security`. In this case, we want the view to be accessible form
`/admin/config` and require authentication, so:

~~~python
from flask import Blueprint
from flask.ext.security import login_required
from flask.ext.waffleconf import register_waffle

# Define the admin Blueprint
admin = Blueprint('admin', __name__)

# Register the view
register_waffle(admin, 'config', '/config', [login_required,])

# Add Blueprint to application
app.register_blueprint(admin, url_prefix='/admin')
~~~
