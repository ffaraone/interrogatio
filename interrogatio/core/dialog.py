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

from ..utils.constants import InputMode
from ..utils.registries import get_input_handlers_registry
from ..themes import get_theme_manager
from ..validators import Validator


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