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

from ..themes import get_theme_manager
from ..validators import ValidationContext, ValidationError
from ..widgets import SelectOne, SelectMany
from ..enums import Mode

from .base import Handler


class ValueHandler(Handler):
   
    ALIAS = 'input'

    def __init__(self, *args, **kwargs):
        super(ValueHandler, self).__init__(*args, **kwargs)
        self.widget = TextArea(**self.get_kwargs())


    def get_kwargs(self):
        kwargs = dict(
            multiline=False,
            style='class:{}.input.answer'.format(self._mode)
        )
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_value(self):
        return self.widget.text

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        align = HorizontalAlign.LEFT
        if self._mode == Mode.DIALOG:
            align = HorizontalAlign.JUSTIFY

        return VSplit([
                Label(
                    msg,
                    dont_extend_width=True,
                    style='class:{}.input.question'.format(self._mode)),
                self.widget
            ], padding=1, align=align)

    def get_app(self):
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        @bindings.add(Keys.Enter)
        def _enter(event):
            get_app().exit(result=self.get_answer())


        return Application(
            layout=Layout(self.get_layout()),
            key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
            style=get_theme_manager().get_current_style())


class PasswordHandler(ValueHandler):

    ALIAS = 'password'

    def __init__(self, *args, **kwargs):
        super(PasswordHandler, self).__init__(*args, **kwargs)
        self.widget = TextArea(**self.get_kwargs())

    def get_kwargs(self):
        kwargs = dict(
            multiline=False,
            style='class:{}.password.answer'.format(self._mode),
            password=True
        )
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_value(self):
        return self.widget.text

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        align = HorizontalAlign.LEFT
        if self._mode == Mode.DIALOG:
            align = HorizontalAlign.JUSTIFY

        return VSplit([
                Label(
                    msg,
                    dont_extend_width=True,
                    style='class:{}.password.question'.format(self._mode)),
                self.widget
            ], padding=1, align=align)

    def get_app(self):
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        @bindings.add(Keys.Enter)
        def _enter(event):
            get_app().exit(result=self.get_answer())


        return Application(
            layout=Layout(self.get_layout()),
            key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
            style=get_theme_manager().get_current_style())




class SelectOneHandler(Handler):

    ALIAS = 'selectone'

    def __init__(self, *args, **kwargs):
        super(SelectOneHandler, self).__init__(*args, **kwargs)
        self.widget = SelectOne(**self.get_kwargs())

    def get_value(self):
        return self.widget.current_value

    def get_kwargs(self):
        kwargs = dict(
            values=self._question['values'],
            style='class:{}.selectone.answer'.format(self._mode)
        )
        if 'default' in self._question:
            kwargs['default'] = self._question['default']

        return kwargs

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        
        return HSplit([
            Label(msg, style='class:{}.selectone.question'.format(self._mode)),
            self.widget
        ])

    def get_app(self):

        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        def accept_handler(value):
            get_app().exit(result=self.get_answer())
        
        self.widget.accept_handler = accept_handler

        return Application(
            layout=Layout(self.get_layout()),
            key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
            style=get_theme_manager().get_current_style())


class SelectManyHandler(Handler):

    ALIAS = 'selectmany'

    def __init__(self, *args, **kwargs):
        super(SelectManyHandler, self).__init__(*args, **kwargs)
        self.widget = SelectMany(**self.get_kwargs())

    def get_value(self):
        return list(self.widget.checked)

    def get_kwargs(self):
        kwargs = dict(
            values=self._question['values'],
            style='class:{}.selectmany.answer'.format(self._mode)
        )
        if 'default' in self._question:
            kwargs['default'] = self._question['default']

        return kwargs

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        
        return HSplit([
            Label(msg, style='class:{}.selectmany.question'.format(self._mode)),
            self.widget
        ])

    def get_app(self):

        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        def accept_handler(value):
            get_app().exit(result=self.get_answer())
        
        self.widget.accept_handler = accept_handler

        return Application(
            layout=Layout(self.get_layout()),
            key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
            style=get_theme_manager().get_current_style())