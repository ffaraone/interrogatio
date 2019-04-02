Reference
=========

Core functions
--------------

.. automodule:: interrogatio
    :members: interrogatio, dialogus


QHandlers
---------
A QHandler is a question handler. It provides the question UI layout, handle
the answer and optionally defines custom key bindings.
QHandler subclasses must be registered within interrogatio, so it
can be instantiated by its aliases.

.. automodule:: interrogatio.handlers
    :members: register, get_instance, get_registered

.. autoclass:: interrogatio.handlers.QHandler
    :members:


Validators
----------
Validators validate the answer to a question.
Validator subclasses must be registered within interrogatio, so it
can be instantiated by its aliases.

.. automodule:: interrogatio.validators
    :members: register, get_instance, get_registered

.. autoclass:: interrogatio.validators.Validator
    :members: __init__, validate

.. .. autoclass:: interrogatio.validators.ValidationError

.. .. autoclass:: interrogatio.validators.Validator
..     :members: __init__, validate

.. .. autoclass:: interrogatio.validators.RequiredValidator
..     :members: __init__

.. .. autoclass:: interrogatio.validators.RegexValidator
..     :members: __init__

.. .. autoclass:: interrogatio.validators.EmailValidator
..     :members: __init__

.. .. autoclass:: interrogatio.validators.URLValidator
..     :members: __init__

.. .. autoclass:: interrogatio.validators.MinLengthValidator
..     :members: __init__

.. .. autoclass:: interrogatio.validators.MaxLengthValidator
..     :members: __init__
