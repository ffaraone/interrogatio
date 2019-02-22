Reference
=========

Core functions
--------------

.. automodule:: interrogatio
    :members: interrogatio, dialogus


Input handlers
--------------

.. autoclass:: interrogatio.handlers.InputHandler
    :members: get_style_rules_names, get_style, get_input, apply_validators


Validators
----------

.. autoclass:: interrogatio.validators.ValidationError

.. autoclass:: interrogatio.validators.Validator
    :members: __init__, validate

.. autoclass:: interrogatio.validators.RequiredValidator
    :members: __init__

.. autoclass:: interrogatio.validators.RegexValidator
    :members: __init__

.. autoclass:: interrogatio.validators.EmailValidator
    :members: __init__

.. autoclass:: interrogatio.validators.URLValidator
    :members: __init__

.. autoclass:: interrogatio.validators.MinLengthValidator
    :members: __init__

.. autoclass:: interrogatio.validators.MaxLengthValidator
    :members: __init__
