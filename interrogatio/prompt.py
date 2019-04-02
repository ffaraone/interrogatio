from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.layout import HorizontalAlign, Layout
from prompt_toolkit.shortcuts import print_formatted_text

from .dialog import show_dialog
from .handlers import get_instance
from .themes import for_prompt, set_theme
from .utils import validate_questions
from .validators import Validator

__all__ = ['interrogatio']

def interrogatio(questions, theme='default'):
    """
    Prompts user for inputs as defined in the questions parameter and returns
    a dictionary with the answers.

    :param questions: a list of questions.
    :type questions: list
    :param theme: the name of the theme to use.
    :type theme: string

    :return: a dictionary with the answers.
    :rtype: dict

    :raise InvalidQuestionError: if there is an error in the question
                                 definition.
    :raise ThemeNotFoundError: if the specified theme does not exists.

    Usage:

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
        answers = interrogatio(questions, theme='purple')
    """
    set_theme(theme)
    answers = {}
    validate_questions(questions)
    for q in questions:
        handler = get_instance(q)
        l = handler.get_layout()
        l.align = HorizontalAlign.LEFT

        bindings = [load_key_bindings()]

        handler_bindings = handler.get_keybindings()

        if handler_bindings:
            bindings.append(handler_bindings)

        app = Application(
            layout=Layout(l),
            key_bindings=merge_key_bindings(bindings),
            style=for_prompt())

        while True:
            app.run()
            if handler.is_valid():
                answers.update(handler.get_answer())
                break
            else:
                print_formatted_text(
                    FormattedText([
                        ('class:error', handler.errors[0])
                    ]),
                    style=for_prompt()
                )
    return answers
