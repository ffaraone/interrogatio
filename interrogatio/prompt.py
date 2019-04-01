from .core.constants import InputMode
from .core.registries import (get_input_handlers_registry,
                              get_validators_registry)
from .dialog import show_dialog
from .themes import get_theme_manager
from .utils import validate_questions
from .validators import Validator


from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, HorizontalAlign
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import print_formatted_text
from .themes import get_theme_manager

__all__ = ['interrogatio']

def interrogatio(questions):
    """
    Prompts user for inputs as defined in the questions parameter and returns
    a dictionary with the answers.

    :param questions: a list of questions.
    :type questions: list
    
    :return: a dictionary with the answers.
    :rtype: dict

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
        answers = interrogatio(questions)
    """

    registry = get_input_handlers_registry()
    answers = {}
    validate_questions(questions)
    for q in questions:
        handler = registry.get_instance(q)
        l = handler.get_layout()
        l.align = HorizontalAlign.LEFT
        app = Application(
            layout=Layout(l),
            key_bindings=handler.get_keybindings(),
            style=get_theme_manager().get_current_theme().for_prompt())
        
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
                    style=get_theme_manager().get_current_theme().for_prompt()
                )
    return answers
