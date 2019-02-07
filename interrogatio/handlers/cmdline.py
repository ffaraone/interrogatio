import abc

import six
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import D, HSplit, Layout, VSplit, HorizontalAlign
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Label, TextArea

from ..themes import get_current_theme
from ..validators import ValidationContext, ValidationError
from ..widgets import RadioList

from .base import Interrogatio

class ValueInterrogatio(Interrogatio):
   
    def get_kwargs(self):
        kwargs = dict()
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_app(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ? ')
        )
        textarea = TextArea(multiline=False, **self.get_kwargs())
        layout = Layout(
            VSplit([
                Label(msg, dont_extend_width=True),
                textarea
            ], padding=2, align=HorizontalAlign.LEFT)
        )

        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        @bindings.add(Keys.Enter)
        def _enter(event):
            get_app().exit(result=textarea.text)


        return Application(
            layout=layout,
            key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
            style=get_current_theme())


class PasswordInterrogatio(ValueInterrogatio):

    def get_kwargs(self):
        return dict(**super().get_kwargs(), password=True)


class SelectOneInterrogatio(Interrogatio):

    def get_kwargs(self):
        kwargs = dict(values=self._question['values'])
        if 'default' in self._question:
            kwargs['text'] = self._question['default']

        return kwargs

    def get_app(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ? ')
        )
        layout = Layout(
            HSplit([
                Label(msg),
                RadioList(**self.get_kwargs())
            ])
        )

        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        return Application(
            layout=layout,
            key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
            style=get_current_theme())


