from ..enums import Mode
from ..handlers import get_handler
from ..themes import get_theme_manager
from ..validators import Validator
from .utils import validate_question
from .dialog import show_dialog

__all__ = [
    'interrogatio'
]


def interrogatio(questions, 
                 dialog=False,
                 title='Please fill the following form',
                 confirm='Ok',
                 cancel='Cancel'):
    answers = {}
    for q in questions:
        validate_question(q)
        if not dialog:
            answers.update(get_handler(
                q,
                questions,
                answers, 
                mode=Mode.PROMPT).get_input())
    if dialog:
        return show_dialog(questions, title, confirm, cancel)
    return answers
