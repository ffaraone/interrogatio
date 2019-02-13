from ..utils.constants import InputMode
from ..utils.registries import get_input_handlers_registry
from ..themes import get_theme_manager
from ..validators import Validator
from .utils import validate_question
from .dialog import show_dialog

__all__ = [
    'interrogatio',
    'dialogus'
]

def _validate_questions(questions):
    for q in questions:
        validate_question(q)

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
    _validate_questions(questions)
    for q in questions:
        answers.update(registry.get_instance(
            q,
            questions,
            answers, 
            mode=InputMode.PROMPT).get_input())
    return answers

def dialogus(
    questions, 
    title='Please fill the following form',
    confirm='Ok',
    cancel='Cancel'):
    _validate_questions(questions)
    return show_dialog(questions, title, confirm, cancel)