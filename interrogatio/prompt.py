from .core.constants import InputMode
from .core.registries import (get_input_handlers_registry,
                              get_validators_registry)
from .dialog import show_dialog
from .themes import get_theme_manager
from .utils import validate_questions
from .validators import Validator

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
        answers.update(registry.get_instance(
            q,
            questions,
            answers, 
            mode=InputMode.PROMPT).get_input())
    return answers
