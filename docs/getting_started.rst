Getting started
===============

Requirements
------------

interrogatio depends on the python-prompt-toolkit library and its dependencies.

Installation
------------

Using pip
^^^^^^^^^

::

    $ pip install interrogatio


Extra dependencies
^^^^^^^^^^^^^^^^^^

If you want to validate password complexity you can install the 
`zxvvbn library <https://github.com/dwolfhub/zxcvbn-python>`_.

::

    $ pip install interrogatio[zxcvbn]

If you want to use the shell command with yml files you can install the yml dependency:


::

    $ pip install interrogatio[yml]


Basic usage
-----------

interrogatio needs a list of questions to prompt the user for answers.

Each question is a python dictionary with at least the following keys:

    * **name**: it has to be unique within the list of questions. It represents the variable name;
    * **type**: the type of question;
    * **message**: the text of the prompt.

Optionally you should specify:
    
    * a **default**: a default value;
    * a **validators**: a list of children of Validator class
    * a **question_mark**: you can customize the question mark symbol.
    * a **values**: a list of tuples (value, label) to provide a list of choices 
      for the ``selectone`` or ``selectmany`` question types.


Each type of question is managed by a :class:`interrogatio.handlers.InputHandler`.

See the :ref:`input_handlers` section for more information. 


Run interrogatio
----------------

As prompts
^^^^^^^^^^

.. code-block:: python

    from interrogatio import interrogatio

    questions = [
        {
            'name': 'name',
            'type': 'input',
            'message': 'What is your name'
        },
        {
            'name': 'favorite_pet',
            'type': 'input',
            'message': 'What is your favorite pet'
        }           
    ]
    answers = interrogatio(questions)


As dialogs
^^^^^^^^^^

.. code-block:: python

    from interrogatio import dialogus

    questions = [
        {
            'name': 'name',
            'type': 'input',
            'message': 'What is your name'
        },
        {
            'name': 'favorite_pet',
            'type': 'input',
            'message': 'What is your favorite pet'
        }           
    ]
    answers = dialogus(
        questions,
        title='Please tell me something about you',
        confirm='ok',
        cancel='cancel')


You can customize the dialog title and the confirm and cancel buttons text.


Validation
----------

You could specify a list of validators for each question:


.. code-block:: python

    from interrogatio import dialogus
    from interrogatio.validators import RequiredValidator, MinLengthValidator

    questions = [
        {
            'name': 'username',
            'type': 'input',
            'message': 'Enter your username',
            'validators': [RequiredValidator()]

        },
        {
            'name': 'password',
            'type': 'password',
            'message': 'Enter your password',
            'validators': [MinLengthValidator(min_length=8)]
        }           
    ]
    answers = dialogus(
        questions,
        title='Please enter your credential',
        confirm='login',
        cancel='cancel')


Validators can also be expressed using aliases:

.. code-block:: python

    from interrogatio import dialogus
    from interrogatio.validators import RequiredValidator, MinLengthValidator

    questions = [
        {
            'name': 'username',
            'type': 'input',
            'message': 'Enter your username',
            'validators': [
                {
                    'name': 'required'
                }
            ]

        },
        {
            'name': 'favorite_pet',
            'type': 'input',
            'message': 'What is your favorite pet',
            'validators': [
                {
                    'name': 'min-length',
                    'args': {
                        'min_length': 8
                    }
                }
            ]
        }           
    ]
    answers = dialogus(
        questions,
        title='Please enter your credential',
        confirm='login',
        cancel='cancel')



This way you can read questions from a json or yaml file.

