import abc

import six
from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.completion import PathCompleter, WordCompleter
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import D, HorizontalAlign, HSplit, Layout, VSplit
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Label, TextArea

from ..core.exceptions import ValidationError
from ..widgets import SelectMany, SelectOne
from .base import QHandler, register


class StringHandler(QHandler):

    def get_widget_class(self):
        return TextArea

    def get_widget_init_kwargs(self):
        kwargs = dict(
            multiline=False,
            style='class:input.answer'
        )
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        widget = self.get_widget()
        widget.buffer.cursor_position = len(widget.text)
        return VSplit([
                Label(
                    msg,
                    dont_extend_width=True,
                    style='class:input.question'),
                widget
            ], padding=1)


    def get_keybindings(self):
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(result=False)

        @bindings.add(Keys.Enter)
        def _enter(event):
            get_app().exit(result=True)
        
        return bindings

    def get_value(self):
        return self.get_widget().text


register('input', StringHandler)



class PasswordHandler(QHandler):

    def get_widget_class(self):
        return TextArea

    def get_widget_init_kwargs(self):
        kwargs = dict(
            multiline=False,
            style='class:password.answer',
            password=True
        )
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_value(self):
        return self.get_widget().text

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        widget = self.get_widget()
        widget.buffer.cursor_position = len(widget.text)

        return VSplit([
                Label(
                    msg,
                    dont_extend_width=True,
                    style='class:password.question'),
                widget
            ], padding=1)

    def get_keybindings(self):
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        @bindings.add(Keys.Enter)
        def _enter(event):
            get_app().exit(result=self.get_answer())

        return bindings

register('password', PasswordHandler)


class SelectOneHandler(QHandler):

    def get_widget_class(self):
        return SelectOne

    def get_value(self):
        return self.get_widget().current_value

    def get_widget_init_kwargs(self):
        kwargs = dict(
            values=self._question['values'],
            style='class:selectone.answer'
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
            Label(msg, style='class:selectone.question'),
            self.get_widget()
        ])

    def get_keybindings(self):

        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        def accept_handler(value):
            get_app().exit(result=self.get_answer())
        
        self.get_widget().accept_handler = accept_handler

        return bindings

register('selectone', SelectOneHandler)


class SelectManyHandler(QHandler):


    def get_widget_class(self):
        return SelectMany


    def get_value(self):
        return list(self.get_widget().checked)

    def get_widget_init_kwargs(self):
        kwargs = dict(
            values=self._question['values'],
            style='class:selectmany.answer'
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
            Label(msg, style='class:selectmany.question'),
            self.get_widget()
        ])

    def get_keybindings(self):

        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        def accept_handler(value):
            get_app().exit(result=self.get_answer())
        
        self.get_widget().accept_handler = accept_handler

        return bindings

register('selectmany', SelectManyHandler)

class TextHandler(QHandler):
   
    def get_widget_class(self):
        return TextArea

    
    def get_widget_init_kwargs(self):
        kwargs = dict(
            multiline=True,
            height=4,
            style='class:text.answer'
        )
        if 'rows' in self._question:
            kwargs['height'] = int(self._question['rows'])
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_value(self):
        return self.get_widget().text

    def get_layout(self):
        msg = '{}{}'.format(
            self._question['message'],
            self._question.get('question_mark', ' ?')
        )
        return VSplit([
                Label(
                    msg,
                    dont_extend_width=True,
                    style='class:text.question'),
                self.get_widget()
            ], padding=1)

    def get_keybindings(self):
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(exception=KeyboardInterrupt)

        @bindings.add(Keys.ControlX)
        def _enter(event):
            get_app().exit(result=self.get_answer())

        return bindings


# class PathHandler(ValueHandler):
    
#     ALIAS = 'path'

#     def __init__(self, *args, **kwargs):
#         super(PathHandler, self).__init__(*args, **kwargs)
#         self.widget.completer = PathCompleter()
    

class PathHandler(StringHandler):
    def get_widget(self):
        widget = super(PathHandler, self).get_widget()
        widget.completer = PathCompleter()
        return widget

register('path', PathHandler)
    
# class RePasswordHandler(QHandler):

#     ALIAS = 'repassword'


#     def __init__(self, *args, **kwargs):
#         super(RePasswordHandler, self).__init__(*args, **kwargs)
#         self.widget = TextArea(**self.get_kwargs())
#         self.widget.buffer.cursor_position = len(self.widget.text)
#         self.rewidget = TextArea(**self.get_kwargs())
#         self.rewidget.buffer.cursor_position = len(self.rewidget.text)

#     def get_kwargs(self):
#         kwargs = dict(
#             multiline=False,
#             style='class:{}.{}.answer'.format(self._mode, self.ALIAS),
#             password=True
#         )
#         if 'default' in self._question:
#             kwargs['text'] = self._question['default']
#         return kwargs

#     def get_value(self):
#         return self.widget.text

#     def get_layout(self):
#         msg = '{}{}'.format(
#             self._question['message'],
#             self._question.get('question_mark', ' ?')
#         )
#         align = HorizontalAlign.LEFT
#         if self._mode == InputMode.DIALOG:
#             align = HorizontalAlign.JUSTIFY

#         return HSplit([
#             VSplit([
#                     Label(
#                         msg,
#                         dont_extend_width=True,
#                         style='class:{}.{}.question'.format(self._mode,
#                                                             self.ALIAS)),
#                     self.widget
#                 ], padding=1, align=align),
#             VSplit([
#                     Label(
#                         'Again',
#                         dont_extend_width=True,
#                         style='class:{}.{}.question'.format(self._mode,
#                                                             self.ALIAS)),
#                     self.rewidget
#                 ], padding=1, align=align)
#         ])

#     def get_app(self):
#         bindings = KeyBindings()

#         @bindings.add(Keys.ControlC)
#         def _ctrl_c(event):
#             get_app().exit(exception=KeyboardInterrupt)


#         @bindings.add('tab')
#         def _tab(event):
#             get_app().layout.focus_next()

#         @bindings.add('s-tab')
#         def _stab(event):
#             get_app().layout.focus_previous()

#         @bindings.add(Keys.Enter)
#         def _enter(event):
#             if get_app().layout.has_focus(self.rewidget):
#                 get_app().exit(result=self.get_answer())
#             else:
#                 get_app().layout.focus_next()

#         return Application(
#             layout=Layout(self.get_layout()),
#             key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
#             style=get_theme_manager().get_current_style())

#     def apply_validators(self):
#         validators = self._question.get('validators', [])
#         error_messages = []
#         if self.widget.text != self.rewidget.text:
#             msg = 'Password and repeat password doesn\'t match'
#             error_messages.append(msg)
#             if self._mode == InputMode.PROMPT:
#                 print_formatted_text(
#                     FormattedText([
#                         ('class:prompt.error', msg)
#                     ]),
#                     style=get_theme_manager().get_current_style()
#                 )
#         for validator in validators:
#             try:
#                 validator.validate(self.get_value(), self._context)
#             except ValidationError as ve:
#                 error_messages.append(ve.message)
#                 if self._mode == InputMode.PROMPT:
#                     print_formatted_text(
#                         FormattedText([
#                             ('class:prompt.error', ve.message)
#                         ]),
#                         style=get_theme_manager().get_current_style()
#                     )
#         return error_messages