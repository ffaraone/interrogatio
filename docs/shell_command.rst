Shell command
=============

Interrogatio ships with a shell command that can be usefull for shell
scripting.
Questions can be provided both as a json or yaml file (Needs pyYAML).

Usage
-----

Prompt mode
^^^^^^^^^^^

.. code-block::bash

    $ interrogatio --help


usage: interrogatio [-h] --input INPUT [--output OUTPUT] [--input-format {json,yaml}] [--output-format {json,yaml}] [--theme THEME]

Prompt user for questions.

optional arguments:
-h, --help            show this help message and exit
--input INPUT, -i INPUT
                        Input file with questions
--output OUTPUT, -o OUTPUT
                        Output file to write answers to (Default: STDOUT)
--input-format {json,yaml}
                        Questions file format (Default: json)
--output-format {json,yaml}
                        Answers file format (Default: json)
--theme THEME, -t THEME
                        Name of the UI theme to use (Default: default)



Dialog mode
^^^^^^^^^^^

..code-block:: bash

    $ dialogus --help


usage: dialogus [-h] --input INPUT [--output OUTPUT] [--input-format {json,yaml}] [--output-format {json,yaml}] [--theme THEME] [--title TITLE] [--intro INTRO]
                [--summary] [--previous PREVIOUS] [--next NEXT] [--cancel CANCEL] [--finish FINISH]

Show a wizard dialog to prompt user for questions.

optional arguments:
-h, --help            show this help message and exit
--input INPUT, -i INPUT
                        Input file with questions
--output OUTPUT, -o OUTPUT
                        Output file to write answers to (Default: STDOUT)
--input-format {json,yaml}
                        Questions file format (Default: json)
--output-format {json,yaml}
                        Answers file format (Default: json)
--theme THEME, -t THEME
                        Name of the UI theme to use (Default: default)
--title TITLE         Title of the dialog
--intro INTRO         Specify the text of the introduction step (Default: no intro)
--summary             Show a summary with answers as the latest step (Default: no summary)
--previous PREVIOUS   Customize the text of the "previous" button (Default: Previous)
--next NEXT           Customize the text of the "next" button (Default: Next)
--cancel CANCEL       Customize the text of the "cancel" button (Default: Cancel)
--finish FINISH       Customize the text of the "finish" button (Default: Finish)
