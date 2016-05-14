Usage in views
==============

Since *version 0.3.0* the extension does not impose a specific view or template
to use. Instead, you can implement your own views and work with the
:py:meth:`~flask_waffleconf.core._WaffleState` instance in the application.

Initialization
--------------

To initialize the extension, two different things are required: a model
implementing the :py:class:`~flask_waffleconf.models.WaffleMixin` interface,
for instance using SQLAlchemy or peewee; and a configured
:py:class:`~flask_waffleconf.store.WaffleStore`.

As of *version 0.3.0*, there are two stores available (although it is very easy
to create a new one using the ``WaffleStore`` class as a base):

- :py:class:`~flask_waffleconf.store.AlchemyWaffleStore`: uses ``SQLAlchemy``
    for the database backend
- :py:class:`~flask_waffleconf.store.PeeweeWaffleStore`: uses ``peewee``
    for the database backend

.. note::
   Model and store should use the same ORM/library as backend.

Obtaining stored values
-----------------------

The following simple views are an example of how you can use the extension to
parse stored values of configuration variables:

.. code-block:: python

    from flask import current_app

    @app.route('/all')
    def get_all():
        """Returns the whole list of stored configuration variables."""
        state = current_app.extensions['waffleconf']

        # Get all the variables
        parsed = state.parse_conf() # Returns a dict

        return parsed

    @app.route('/<key>')
    def get_key(key):
        """Return the value of a single key."""
        state = current_app.extensions['waffleconf']

        # Get variable
        parsed = state.parse_conf([key,]) # Returns a dict

        return parsed

As the :py:meth:`~flask_waffleconf.core.WaffleState.parse_conf` method returns
a Python ``dict``, creating a form for showing or updating the values is very
easy.

Updating stored values
----------------------

Similarly, it is also possible to update values at runtime using a custom view:

.. code-block:: python

   from flask import current_app, form

    @app.route('/update', methods=['POST'])
    def update_vars():
        """Update the vars with the values of a hypothetical form."""
        # Suppose WTForms with fields `SITENAME` and `DESCRIPTION`
        form = Form(request.form)

        if form.validate():
            vals = {
                'SITENAME': form.sitename.data,
                'DESCRIPTION': form.desc.data
            }

            state = current_app.extensions['waffleconf']
            state.update_db(vals)
