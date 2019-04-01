from prompt_toolkit.shortcuts import button_dialog as pt_button_dialog
from prompt_toolkit.shortcuts import input_dialog as pt_input_dialog
from prompt_toolkit.shortcuts import message_dialog as pt_message_dialog
from prompt_toolkit.shortcuts import progress_dialog as pt_progress_dialog
from prompt_toolkit.shortcuts import radiolist_dialog as pt_radiolist_dialog
from prompt_toolkit.shortcuts import yes_no_dialog as pt_yes_no_dialog

from ..themes import for_dialog

__all__ = [
    'yes_no_dialog',
    'button_dialog',
    'input_dialog',
    'message_dialog',
    'radiolist_dialog',
    'progress_dialog',
]

def yes_no_dialog(title='', text='', yes_text='Yes', no_text='No',
                  style=None, async_=False):
    style = style or for_dialog()
    return pt_yes_no_dialog(title, text, yes_text, no_text,
                            style, async_)

def button_dialog(title='', # pylint: disable=dangerous-default-value
                  text='',
                  buttons=[],
                  style=None,
                  async_=False):
    style = style or for_dialog()
    return pt_button_dialog(title, text, buttons, style, async_)

def input_dialog(title='', text='', ok_text='OK', cancel_text='Cancel',
                 completer=None, password=False, style=None,
                 async_=False):
    style = style or for_dialog()
    return pt_input_dialog(title, text, ok_text, cancel_text,
                           completer, password, style, async_)

def message_dialog(title='', text='', ok_text='Ok',
                   style=None, async_=False):
    style = style or for_dialog()
    return pt_message_dialog(title, text, ok_text, style, async_)

def radiolist_dialog(title='', text='', ok_text='Ok', cancel_text='Cancel',
                     values=None, style=None,
                     async_=False):
    style = style or for_dialog()
    return pt_radiolist_dialog(title, text, ok_text, cancel_text, values,
                               style, async_)

def progress_dialog(title='', text='', run_callback=None,
                    style=None, async_=False):
    style = style or for_dialog()
    return pt_progress_dialog(title, text, run_callback, style, async_)
