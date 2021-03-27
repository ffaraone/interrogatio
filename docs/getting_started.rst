Getting started
===============

Requirements
------------

``interrogatio`` depends on the python-prompt-toolkit library and its dependencies.

Installation
------------

Using pip
^^^^^^^^^

.. code-block:: bash

    $ pip install interrogatio


Extra dependencies
^^^^^^^^^^^^^^^^^^

If you want to use the shell command with yml files you can install the yml dependency:


.. code-block:: bash

    $ pip install interrogatio[yml]


Basic usage
-----------

``interrogatio`` needs a list of questions to prompt the user for answers.

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


Each type of question is managed by a :class:`interrogatio.handlers.QHandler`.

See the :ref:`input_handlers` section for more information. 


Run interrogatio
----------------

Prompt mode
^^^^^^^^^^^

.. image:: showcase/interrogatio.gif

.. code-block:: python

    from interrogatio import interrogatio

    questions = [
        {
            'name': 'name',
            'type': 'input',
            'message': "What's your name ?",
            'description': 'Please enter your full name. This field is required.',
            'validators': [{'name': 'required'}],
        },
        {
            'name': 'birth_date',
            'type': 'date',
            'message': "What's your birth date ?",
            'description': 'Enter your birth date.',
        },
        {
            'name': 'nationality',
            'type': 'selectone',
            'message': "What's your nationality ?",
            'description': 'Please choose one from the list.',
            'validators': [{'name': 'required'}],
            'values': [
                ('IT', 'Italian'),
                ('ES', 'Spanish'),
                ('US', 'American'),
                ('UK', 'English'),
            ],
        },
        {
            'name': 'languages',
            'type': 'selectmany',
            'message': "What are your favorite programming languages ?",
            'description': 'Please choose your favorites from the list.',
            'values': [
                ('py', 'Python'),
                ('rb', 'Ruby'),
                ('js', 'Javascript'),
                ('go', 'Golang'),
                ('rs', 'Rust'),
                ('c', 'C'),
                ('cpp', 'C++'),
                ('java', 'Java'),
            ],
        },
    ]


    answers = interrogatio(questions)


Dialog mode
^^^^^^^^^^^

.. image:: showcase/dialogus.gif

.. code-block:: python

    from interrogatio import dialogus

    questions = [
        {
            'name': 'name',
            'type': 'input',
            'message': "What's your name ?",
            'description': 'Please enter your full name. This field is required.',
            'validators': [{'name': 'required'}],
        },
        {
            'name': 'birth_date',
            'type': 'date',
            'message': "What's your birth date ?",
            'description': 'Enter your birth date.',
        },
        {
            'name': 'nationality',
            'type': 'selectone',
            'message': "What's your nationality ?",
            'description': 'Please choose one from the list.',
            'validators': [{'name': 'required'}],
            'values': [
                ('IT', 'Italian'),
                ('ES', 'Spanish'),
                ('US', 'American'),
                ('UK', 'English'),
            ],
        },
        {
            'name': 'languages',
            'type': 'selectmany',
            'message': "What are your favorite programming languages ?",
            'description': 'Please choose your favorites from the list.',
            'values': [
                ('py', 'Python'),
                ('rb', 'Ruby'),
                ('js', 'Javascript'),
                ('go', 'Golang'),
                ('rs', 'Rust'),
                ('c', 'C'),
                ('cpp', 'C++'),
                ('java', 'Java'),
            ],
        },
    ]

    intro = """<blue>Welcome to <b><i>interrogatio 2.0</i></b>!

    This is the second major release of interrogatio with nice improvements.</blue>

    <b>What's new</b>
    <b>----------</b>

    * Curses-like dialog experience had been completely rewritten.
    * New questions handlers for dates, date ranges and masked inputs.
    * Validators are now based on the <u>validators</u> library.
    """


    answers = dialogus(questions, 'interrogatio showcase', intro=intro, summary=True)


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
            'validators': [MinLengthValidator(8)]
        }  ,         
    ]
    answers = dialogus(
        questions,
        'Please enter your credential',
        finish='login',
        cancel='cancel',
    )


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
        'Please enter your credential',
        finish='login',
        cancel='cancel',
    )



This way you can read questions from a json or yaml file.

