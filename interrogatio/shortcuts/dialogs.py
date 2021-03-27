from prompt_toolkit.shortcuts import button_dialog as pt_button_dialog
from prompt_toolkit.shortcuts import input_dialog as pt_input_dialog
from prompt_toolkit.shortcuts import message_dialog as pt_message_dialog
from prompt_toolkit.shortcuts import progress_dialog as pt_progress_dialog
from prompt_toolkit.shortcuts import radiolist_dialog as pt_radiolist_dialog
from prompt_toolkit.shortcuts import yes_no_dialog as pt_yes_no_dialog

from interrogatio.themes import for_dialog

__all__ = [
    'yes_no_dialog',
    'button_dialog',
    'input_dialog',
    'message_dialog',
    'radiolist_dialog',
    'progress_dialog',
]


def yes_no_dialog(
    title='',
    text='',
    yes_text='Yes',
    no_text='No',
    style=None,
):
    style = style or for_dialog()
    return pt_yes_no_dialog(
        title=title,
        text=text,
        yes_text=yes_text,
        no_text=no_text,
        style=style,
    )


def button_dialog(
    title='',
    text='',
    buttons=None,
    style=None,
):
    style = style or for_dialog()
    return pt_button_dialog(
        title=title,
        text=text,
        buttons=buttons or [],
        style=style,
    )


def input_dialog(
    title='', text='', ok_text='OK', cancel_text='Cancel',
    completer=None, password=False, style=None,
):
    style = style or for_dialog()
    return pt_input_dialog(
        title=title, text=text, ok_text=ok_text,
        cancel_text=cancel_text, completer=completer,
        password=password, style=style,
    )


def message_dialog(
    title='', text='', ok_text='Ok', style=None,
):
    style = style or for_dialog()
    return pt_message_dialog(
        title=title, text=text,
        ok_text=ok_text, style=style,
    )


def radiolist_dialog(
    title='', text='', ok_text='Ok', cancel_text='Cancel',
    values=None, style=None,
):
    style = style or for_dialog()
    return pt_radiolist_dialog(
        title=title, text=text,
        ok_text=ok_text, cancel_text=cancel_text,
        values=values, style=style,
    )


def progress_dialog(
    title='', text='',
    run_callback=None, style=None,
):
    style = style or for_dialog()
    return pt_progress_dialog(
        title=title, text=text,
        run_callback=run_callback, style=style,
    )
