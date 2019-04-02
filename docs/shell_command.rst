Shell command
=============

Interrogatio ships with a shell command that can be usefull for shell
scripting.
Questions can be provided both as a json or yaml file (Needs pyYAML).

Usage
-----

Interrogatio
^^^^^^^^^^^^

::

    $ interrogatio --theme purple --input question.json --output answers.json

If you omit the ``--theme`` argument, it uses the ``default`` theme.
If you omit the ``--output`` argument, it print the answers json to ``stdout``.

You can also specify input and output file format with the ``--input_format``
and ``--output_format`` arguments.


Dialogus
^^^^^^^^

::

    $ dialogus --theme purple \
        --input question.json \
        --output answers.json \
        --title "My Dialog Title" \
        --confirm "Accept" \
        --cancel "Dismiss"


You can customize the title, confirm button text and cancel button text.

