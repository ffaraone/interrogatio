from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout

from interrogatio.core.utils import validate_questions
from interrogatio.handlers import get_instance
from interrogatio.themes import for_dialog, set_theme
from interrogatio.widgets.wizard import WizardDialog


__all__ = ['dialogus']


def show_dialog(
    questions,
    title,
    intro=None,
    summary=False,
    fast_forward=False,
    next_text='Next',
    previous_text='Previous',
    cancel_text='Cancel',
    finish_text='Finish',
):
    handlers = [get_instance(q) for q in questions]
    app = Application(
        layout=Layout(
            WizardDialog(
                title, handlers,
                intro=intro, summary=summary, fast_forward=fast_forward,
                next_text=next_text, previous_text=previous_text,
                cancel_text=cancel_text, finish_text=finish_text,
            ),
        ),
        mouse_support=True,
        style=for_dialog(),
        full_screen=True,
    )

    if not app.run():
        return
    answers = {}
    for handler in handlers:
        if not handler.is_disabled(answers):
            answers.update(handler.get_answer())
    return answers


def dialogus(
    questions,
    title,
    intro=None,
    summary=False,
    fast_forward=False,
    next_text='Next',
    previous_text='Previous',
    cancel_text='Cancel',
    finish_text='Finish',
    theme='default',
):
    """
    Show a dialog with inputs as defined in the questions parameter and returns
    a dictionary with the answers.

    :param questions: a list of questions.
    :type questions: list

    :param title: the title of the dialog.
    :type title: str

    :param confirm: the confirm button text.
    :type confirm: str

    :param cancel: the cancel button text.
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
            finish_text='Done',
            cancel_text='Cancel',
        )
    """
    set_theme(theme)
    validate_questions(questions)
    return show_dialog(
        questions,
        title,
        intro=intro,
        summary=summary,
        fast_forward=fast_forward,
        next_text=next_text,
        previous_text=previous_text,
        cancel_text=cancel_text,
        finish_text=finish_text,
    )
