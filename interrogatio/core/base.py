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
    """
    Show a dialog with inputs as defined in the questions parameter and returns
    a dictionary with the answers.

    :param questions: a list of questions.
    :type questions: list
    
    :param title: the title of the dialog. *default: Please fill the following form*
    :type title: str

    :param confirm: the confirm button text. *default: Ok*
    :type confirm: str

    :param cancel: the cancel button text. *default: Cancel*
    :type cancel: str   

    :return: a dictionary with the answers.
    :rtype: dict

    Usage:
    
    .. code-block:: python
    
        from interrogatio import dialogus
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
        answers = dialogus(
            questions,
            title='Tell me something about you',
            confirm='Done',
            cancel='Skip')
    """
    _validate_questions(questions)
    return show_dialog(questions, title, confirm, cancel)