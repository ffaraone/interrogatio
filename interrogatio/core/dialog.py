from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding.bindings.focus import (focus_next,
                                                       focus_previous)
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import (KeyBindings,
                                                     merge_key_bindings)
from prompt_toolkit.layout import HSplit, Layout
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.widgets import Button, Dialog

from ..enums import Mode
from ..handlers import get_handler
from ..themes import get_theme_manager
from ..validators import Validator



def show_dialog(questions, title, confirm, cancel):

    handlers = []

    for q in questions:
        handler = get_handler(q, questions, None, mode=Mode.DIALOG)
        handlers.append(handler)

    def ok_handler():
        result = dict()
        for handler in handlers:
            result.update(handler.get_answer())
        get_app().exit(result=result)

    dialog = Dialog(
        title=title,
        body=HSplit([
            h.get_layout() for h in handlers
        ], padding=1),      
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
        
        message_dialog(title='Errors', text='\n'.join(validation_errors))