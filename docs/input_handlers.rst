.. _input_handlers:

Input handlers
==============

interrogatio |release| has these built-in type of handlers:

    * **input**: for strings and numbers
    * **password**: for password
    * **selectone**: like a radio list, users have to choose one value from a
      list of choices.
    * **selectmany**: like a checkbox list, users can choose multiple values
      within a list of choices.


input
-----

The ``input`` handler prompts the user for a string or a number.
You can provide it with a default value.


password
--------

The ``password`` handler hides the user input with an asterisk symbol.

selectone
---------

The ``selectone`` handler allow the user to choose from a list of values.
To choose a value, users can move up and down the list with the arrow keys,
select a value using the space key and accept the answer using the enter key.

The list of values to choose from must be provided as a list of tuples
(or two element lists) where, like a html radio input, the first element
of the tuple is the value and the second one is the label.


selectmany
----------

The ``selectone`` handler allow the user to choose multiple answers from a
list of values.

To choose a value, users can move up and down the list with the arrow keys,
select a value using the space key and accept the answer using the enter key.

The list of values to choose from must be provided as a list of tuples
(or two element lists) where, like a html radio input, the first element
of the tuple is the value and the second one is the label.

This input handler return a list with the chosen values.


