import abc

import six
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import D, HorizontalAlign, HSplit, Layout, VSplit
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Label, TextArea

from ..core.constants import InputMode
from ..core.styles import Rule
from ..core.validation import ValidationContext
from ..themes import get_theme_manager
from ..validators import ValidationError
from ..widgets import SelectMany, SelectOne
from .base import InputHandler


class ValueHandler(InputHandler):
   
    ALIAS = 'input'

    @staticmethod
    def get_style_rules_names():
        return ('question, answer')

    @staticmethod
    def get_style(mode, rules):
        if mode == InputMode.PROMPT:
            question = rules.get('question', Rule(fg='darkblue'))
            answer = rules.get('answer', Rule(fg='orange', attr='bold'))
        else:
            question = rules.get('question', Rule(fg='darkblue', bg='#eeeeee'))
            answer = rules.get('answer', Rule(fg='orange', bg='#eeeeee', 
                                              attr='bold'))

        return [
            ('{}.input.question'.format(mode), str(question)),
            ('{}.input.answer'.format(mode), str(answer))
        ]  


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

    @staticmethod
    def get_style_rules_names():
        return ('question, answer')

    @staticmethod
    def get_style(mode, rules):
        if mode == InputMode.PROMPT:
            question = rules.get('question', Rule(fg='darkblue'))
            answer = rules.get('answer', Rule(fg='orange', attr='bold'))
        else:
            question = rules.get('question', Rule(fg='darkblue', bg='#eeeeee'))
            answer = rules.get('answer', Rule(fg='orange', bg='#eeeeee', 
                                              attr='bold'))

        return [
            ('{}.password.question'.format(mode), str(question)),
            ('{}.password.answer'.format(mode), str(answer))
        ]  


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




class SelectOneHandler(InputHandler):

    ALIAS = 'selectone'

    @staticmethod
    def get_style_rules_names():
        return ('question, answer', 'selected', 'checked')

    @staticmethod
    def get_style(mode, rules):
        if mode == InputMode.PROMPT:
            question = rules.get('question', Rule(fg='darkblue'))
            answer = rules.get('answer', Rule(fg='darkblue', attr='bold'))
            selected = rules.get('selected', Rule(fg='cyan'))
            checked = rules.get('checked', Rule(fg='orange', attr='bold'))
        else:
            question = rules.get('question', Rule(fg='darkblue', bg='#eeeeee'))
            answer = rules.get('answer', Rule(fg='darkblue', bg='#eeeeee',
                                              attr='bold'))
            selected = rules.get('selected', Rule(fg='cyan', bg='#eeeeee'))
            checked = rules.get('checked', Rule(fg='orange', bg='#eeeeee', 
                                           attr='bold'))

        return [
            ('{}.selectone.question'.format(mode), str(question)),
            ('{}.selectone.answer'.format(mode), str(answer)),
            ('{}.selectone.answer radio'.format(mode), str(answer)),
            ('{}.selectone.answer radio-selected'.format(mode), str(selected)),
            ('{}.selectone.answer radio-checked'.format(mode), str(checked))
        ]



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


class SelectManyHandler(InputHandler):

    ALIAS = 'selectmany'

    @staticmethod
    def get_style_rules_names():
        return ('question, answer', 'selected', 'checked')

    @staticmethod
    def get_style(mode, rules):
        if mode == InputMode.PROMPT:
            question = rules.get('question', Rule(fg='darkblue'))
            answer = rules.get('answer', Rule(fg='darkblue', attr='bold'))
            selected = rules.get('selected', Rule(fg='cyan'))
            checked = rules.get('checked', Rule(fg='orange', attr='bold'))
        else:
            question = rules.get('question', Rule(fg='darkblue', bg='#eeeeee'))
            answer = rules.get('answer', Rule(fg='darkblue', bg='#eeeeee',
                                              attr='bold'))
            selected = rules.get('selected', Rule(fg='cyan', bg='#eeeeee'))
            checked = rules.get('checked', Rule(fg='orange', bg='#eeeeee', 
                                           attr='bold'))

        return [
            ('{}.selectmany.question'.format(mode), str(question)),
            ('{}.selectmany.answer'.format(mode), str(answer)),
            ('{}.selectmany.answer checkbox'.format(mode), str(answer)),
            ('{}.selectmany.answer checkbox-selected'.format(mode), str(selected)),
            ('{}.selectmany.answer checkbox-checked'.format(mode), str(checked))
        ]

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


class TextHandler(InputHandler):
   
    ALIAS = 'text'

    @staticmethod
    def get_style_rules_names():
        return ('question, answer')

    @staticmethod
    def get_style(mode, rules):
        if mode == InputMode.PROMPT:
            question = rules.get('question', Rule(fg='darkblue'))
            answer = rules.get('answer', Rule(fg='orange', attr='bold'))
        else:
            question = rules.get('question', Rule(fg='darkblue', bg='#eeeeee'))
            answer = rules.get('answer', Rule(fg='orange', bg='#eeeeee', 
                                              attr='bold'))

        return [
            ('{}.text.question'.format(mode), str(question)),
            ('{}.text.answer'.format(mode), str(answer))
        ]  


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
