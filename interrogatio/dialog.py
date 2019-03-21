from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding.bindings.focus import (focus_next,
                                                       focus_previous)
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import (KeyBindings,
                                                     merge_key_bindings)
from prompt_toolkit.layout import HSplit, Layout, Window
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.widgets import Button, Dialog, Label

from .core.constants import InputMode
from .core.registries import get_input_handlers_registry
from .themes import get_theme_manager
from .utils import validate_questions
from .validators import Validator

__all__ = ['dialogus']

def show_error_dialog(messages):
    texts = []
    for message in messages:
        texts.append(
            Label(message, style='class:dialog.error', dont_extend_height=True)
        )
    dialog = Dialog(
        title='Some inputs are invalid',
        body=HSplit(
            texts,
            padding=1
        ),      
        buttons=[
            Button(text='Ok', handler=lambda: get_app().exit()),
        ],
        with_background=True)


    app = Application(
        layout=Layout(dialog),
        key_bindings=load_key_bindings(),
        mouse_support=True,
        style=get_theme_manager().get_current_style(),
        full_screen=True)

    app.run()

def show_dialog(questions, title, confirm, cancel):

    handlers = []
    registry = get_input_handlers_registry()
    for q in questions:
        handler = registry.get_instance(
            q, questions, None, mode=InputMode.DIALOG)
        handlers.append(handler)

    def ok_handler():
        result = dict()
        for handler in handlers:
            result.update(handler.get_answer())
        get_app().exit(result=result)

    dialog = Dialog(
        title=title,
        body=HSplit(
            [h.get_layout() for h in handlers], 
            padding=1
        ),      
        buttons=[
            Button(text=confirm, handler=ok_handler),
            Button(text=cancel, handler=lambda: get_app().exit()),
        ],
        with_background=True)

    # Key bindings.
    bindings = KeyBindings()
    bindings.add('tab')(focus_next)
    bindings.add('s-tab')(focus_previous)

    app = Application(
        layout=Layout(dialog),
        key_bindings=merge_key_bindings([
            load_key_bindings(),
            bindings,
        ]),
        mouse_support=True,
        style=get_theme_manager().get_current_style(),
        full_screen=True)

    size = app.renderer.output.get_size()
    container = app.layout.container
    height = container.preferred_height(size.columns, size.rows).preferred
    if height > size.rows:
        message_dialog(
            title='Too many questions',
            text='Cannot render a {} rows dialog in a '
                 '{} rows screen: too many questions!'.format(height, 
                                                              size.rows),
            ok_text='Got it!'
        )
        return

    while True:
        validation_errors = []
        answers = app.run()
        if answers is None:
            return
        for handler in handlers:
            for msg in handler.apply_validators():
                validation_errors.append(
                    '{}: {}'.format(
                        handler.get_variable_name(),
                        msg
                    )
                )
        if not validation_errors:
            return answers
        
        show_error_dialog(validation_errors)

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
    validate_questions(questions)
    return show_dialog(questions, title, confirm, cancel)
