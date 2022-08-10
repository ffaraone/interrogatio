from prompt_toolkit.application import Application
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import merge_key_bindings
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.layout import HorizontalAlign, Layout
from prompt_toolkit.shortcuts import print_formatted_text

from interrogatio.core.utils import validate_questions
from interrogatio.handlers import get_instance
from interrogatio.themes import for_prompt, set_theme


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
        if handler.is_disabled(context=answers):
            continue
        handler.set_context(answers)
        layout = handler.get_layout()
        layout.align = HorizontalAlign.LEFT

        bindings = [load_key_bindings()]

        handler_bindings = handler.get_keybindings()

        if handler_bindings:  # pragma: no branch
            bindings.append(handler_bindings)

        app = Application(
            layout=Layout(layout),
            key_bindings=merge_key_bindings(bindings),
            style=for_prompt(),
        )

        while True:
            result = app.run()
            if not result:
                return
            if handler.is_valid(answers):
                answers.update(handler.get_answer())
                break
            else:
                print_formatted_text(
                    FormattedText([('class:error', handler.errors[0])]),
                    style=for_prompt(),
                )
    return answers
