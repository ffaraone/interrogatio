import abc

import six
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.completion import PathCompleter, WordCompleter
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import D, HorizontalAlign, HSplit, Layout, VSplit
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Label, TextArea

from ..core.constants import InputMode
from ..core.styles import to_style_token
from ..core.validation import ValidationContext
from ..themes import get_theme_manager
from ..validators import ValidationError
from ..widgets import SelectMany, SelectOne
from .base import QHandler


class ValueHandler(QHandler):
   
    ALIAS = 'input'


    def __init__(self, *args, **kwargs):
        super(ValueHandler, self).__init__(*args, **kwargs)
        self.widget = TextArea(**self.get_kwargs())
        self.widget.buffer.cursor_position = len(self.widget.text)

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
        if self._mode == InputMode.DIALOG:
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
        self.widget.buffer.cursor_position = len(self.widget.text)

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
        if self._mode == InputMode.DIALOG:
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




class SelectOneHandler(QHandler):

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


class SelectManyHandler(QHandler):

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
        if 'checked' in self._question:
            kwargs['checked'] = set(self._question['checked'])
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


class TextHandler(QHandler):
   
    ALIAS = 'text'


    def __init__(self, *args, **kwargs):
        super(TextHandler, self).__init__(*args, **kwargs)
        self.widget = TextArea(**self.get_kwargs())


    def get_kwargs(self):
        kwargs = dict(
            multiline=True,
            height=4,
            style='class:{}.text.answer'.format(self._mode)
        )
        if 'rows' in self._question:
            kwargs['height'] = int(self._question['rows'])
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
        if self._mode == InputMode.DIALOG:
            align = HorizontalAlign.JUSTIFY

        return VSplit([
                Label(
                    msg,
                    dont_extend_width=True,
                    style='class:{}.text.question'.format(self._mode)),
                self.widget
            ], padding=1, align=align)

    def get_app(self):
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        @bindings.add(Keys.ControlX)
        def _enter(event):
            get_app().exit(result=self.get_answer())

        return Application(
            layout=Layout(self.get_layout()),
            key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
            style=get_theme_manager().get_current_style())


class PathHandler(ValueHandler):
    
    ALIAS = 'path'

    def __init__(self, *args, **kwargs):
        super(PathHandler, self).__init__(*args, **kwargs)
        self.widget.completer = PathCompleter()
    

    
class RePasswordHandler(QHandler):

    ALIAS = 'repassword'


    def __init__(self, *args, **kwargs):
        super(RePasswordHandler, self).__init__(*args, **kwargs)
        self.widget = TextArea(**self.get_kwargs())
        self.widget.buffer.cursor_position = len(self.widget.text)
        self.rewidget = TextArea(**self.get_kwargs())
        self.rewidget.buffer.cursor_position = len(self.rewidget.text)

    def get_kwargs(self):
        kwargs = dict(
            multiline=False,
            style='class:{}.{}.answer'.format(self._mode, self.ALIAS),
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
        if self._mode == InputMode.DIALOG:
            align = HorizontalAlign.JUSTIFY

        return HSplit([
            VSplit([
                    Label(
                        msg,
                        dont_extend_width=True,
                        style='class:{}.{}.question'.format(self._mode,
                                                            self.ALIAS)),
                    self.widget
                ], padding=1, align=align),
            VSplit([
                    Label(
                        'Again',
                        dont_extend_width=True,
                        style='class:{}.{}.question'.format(self._mode,
                                                            self.ALIAS)),
                    self.rewidget
                ], padding=1, align=align)
        ])

    def get_app(self):
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)


        @bindings.add('tab')
        def _tab(event):
            get_app().layout.focus_next()

        @bindings.add('s-tab')
        def _stab(event):
            get_app().layout.focus_previous()

        @bindings.add(Keys.Enter)
        def _enter(event):
            if get_app().layout.has_focus(self.rewidget):
                get_app().exit(result=self.get_answer())
            else:
                get_app().layout.focus_next()

        return Application(
            layout=Layout(self.get_layout()),
            key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
            style=get_theme_manager().get_current_style())

    def apply_validators(self):
        validators = self._question.get('validators', [])
        error_messages = []
        if self.widget.text != self.rewidget.text:
            msg = 'Password and repeat password doesn\'t match'
            error_messages.append(msg)
            if self._mode == InputMode.PROMPT:
                print_formatted_text(
                    FormattedText([
                        ('class:prompt.error', msg)
                    ]),
                    style=get_theme_manager().get_current_style()
                )
        for validator in validators:
            try:
                validator.validate(self.get_value(), self._context)
            except ValidationError as ve:
                error_messages.append(ve.message)
                if self._mode == InputMode.PROMPT:
                    print_formatted_text(
                        FormattedText([
                            ('class:prompt.error', ve.message)
                        ]),
                        style=get_theme_manager().get_current_style()
                    )
        return error_messages
