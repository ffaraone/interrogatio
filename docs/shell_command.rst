Shell command
=============

Interrogatio ships with a shell command that can be usefull for shell scripting.
Questions can be provided both as a json or yaml file.

Usage
-----

::

    $ interrogatio --input question.json --output answers.json


If you omit the ``--òutput`` argument, it print the answers json to ``stdout``.

You can also specify input and output file format with the ``--input_format`` and
``--output_format`` arguments.

If you want to show a dialog:

::

    $ interrogatio --input question.json --output answers.json dialog \
        --title "My Dialog Ttitle" \
        --confirm "Accept" \
        --cancel "Dismiss"


You can customize the title, confirm button text and cancel button text.

