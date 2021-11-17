# pylint: disable=unused-argument
import string

from prompt_toolkit.application.current import get_app
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import HSplit, VSplit
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.widgets import Box, Button, Label, TextArea

from interrogatio.handlers.base import QHandler
from interrogatio.handlers.registry import register
from interrogatio.widgets import DateRange, MaskedInput, SelectMany, SelectOne


@register('input')
class StringHandler(QHandler):

    def get_widget_class(self):
        return TextArea

    def get_widget_init_kwargs(self):
        kwargs = dict(
            multiline=self._question.get('multiline', False),
            style='class:input.answer',
        )
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_layout(self):
        widget = self.get_widget()
        widget.buffer.cursor_position = len(widget.text)
        vsplit_components = [widget]
        if 'message' in self._question and self._question['message']:
            vsplit_components.insert(
                0,
                Label(
                    self._question['message'],
                    dont_extend_width=True,
                    style='class:input.question',
                ),
            )
        hsplit_components = [VSplit(vsplit_components, padding=1)]
        if 'description' in self._question and self._question['description']:
            hsplit_components.insert(
                0,
                Label(
                    self._question['description'],
                    style='class:input.question',
                ),
            )
        return HSplit(hsplit_components, padding=1)

    def get_value(self):
        return self.get_widget().text


@register('password')
class PasswordHandler(QHandler):

    def get_widget_class(self):
        return TextArea

    def get_widget_init_kwargs(self):
        kwargs = dict(
            multiline=False,
            style='class:password.answer',
            password=True,
        )
        if 'default' in self._question:
            kwargs['text'] = self._question['default']
        return kwargs

    def get_value(self):
        return self.get_widget().text

    def get_layout(self):
        widget = self.get_widget()
        widget.buffer.cursor_position = len(widget.text)

        vsplit_components = [widget]
        if 'message' in self._question and self._question['message']:
            vsplit_components.insert(
                0,
                Label(
                    self._question['message'],
                    dont_extend_width=True,
                    style='class:password.question',
                ),
            )
        hsplit_components = [VSplit(vsplit_components, padding=1)]
        if 'description' in self._question and self._question['description']:
            hsplit_components.insert(
                0,
                Label(
                    self._question['description'],
                    style='class:password.question',
                ),
            )
        return HSplit(hsplit_components, padding=1)


@register('selectone')
class SelectOneHandler(QHandler):

    def get_widget_class(self):
        return SelectOne

    def get_value(self):
        return self.get_widget().current_value

    def get_widget_init_kwargs(self):
        kwargs = dict(
            values=self._question['values'],
            style='class:selectone.answer',
        )
        if 'default' in self._question:
            kwargs['default'] = self._question['default']

        return kwargs

    def get_layout(self):
        vsplit_components = [self.get_widget()]
        if 'message' in self._question and self._question['message']:
            vsplit_components.insert(
                0,
                Label(
                    self._question['message'],
                    dont_extend_width=True,
                    dont_extend_height=False,
                    style='class:selectone.question',
                ),
            )
        hsplit_components = [VSplit(vsplit_components, padding=1)]
        if 'description' in self._question and self._question['description']:
            hsplit_components.insert(
                0,
                Label(
                    self._question['description'],
                    style='class:selectone.question',
                ),
            )
        return HSplit(hsplit_components, padding=1)

    def get_formatted_value(self):
        value = self.get_value()
        options = {t[0]: t[1] for t in self._question['values']}
        return f'{options[value]} ({value})'


@register('selectmany')
class SelectManyHandler(QHandler):

    def get_widget_class(self):
        return SelectMany

    def get_value(self):
        return list(self.get_widget().checked)

    def get_widget_init_kwargs(self):
        kwargs = dict(
            values=self._question['values'],
            style='class:selectmany.answer',
        )
        if 'checked' in self._question:
            kwargs['checked'] = set(self._question['checked'])
        if 'default' in self._question:
            kwargs['default'] = self._question['default']

        return kwargs

    def get_layout(self):
        widget = self.get_widget()
        vsplit_components = [widget]
        if 'message' in self._question and self._question['message']:
            vsplit_components.insert(
                0,
                Label(
                    self._question['message'],
                    dont_extend_width=True,
                    dont_extend_height=False,
                    style='class:selectone.question',
                ),
            )

        btn_all = Button('All', widget.select_all)
        btn_none = Button('None', widget.select_none)
        buttons = Box(
            body=VSplit([btn_all, btn_none], padding=1),
            height=D(min=1, max=3, preferred=3),
            padding_left=0,
        )

        hsplit_components = [buttons, VSplit(vsplit_components, padding=1)]
        if 'description' in self._question and self._question['description']:
            hsplit_components.insert(
                0,
                Label(
                    self._question['description'],
                    style='class:selectone.question',
                ),
            )
        return HSplit(hsplit_components, padding=1)

    def get_keybindings(self):

        bindings = super().get_keybindings()

        @bindings.add(Keys.Tab)
        def _tab(event):
            get_app().layout.focus_next()

        @bindings.add(Keys.BackTab)
        def _s_tab(event):
            get_app().layout.focus_previous()

        return bindings

    def get_formatted_value(self):
        values = self.get_value()
        if not values:
            return ''
        options = {t[0]: t[1] for t in self._question['values']}

        formatted_values = []

        for idx, value in enumerate(values):
            if idx > 14:
                formatted_values.append('...')
                break
            formatted_values.append(f'{options[value]} ({value})')

        return ', '.join(formatted_values)


@register('maskedinput')
class MaskedInputHandler(QHandler):

    def get_widget_class(self):
        return MaskedInput

    def get_widget_init_kwargs(self):
        kwargs = dict(
            style='class:input.answer',
            mask=self._question['mask'],
        )
        return kwargs

    def get_layout(self):
        widget = self.get_widget()
        vsplit_components = [widget]
        if 'message' in self._question and self._question['message']:
            vsplit_components.insert(
                0,
                Label(
                    self._question['message'],
                    dont_extend_width=True,
                    style='class:input.question',
                ),
            )
        hsplit_components = [VSplit(vsplit_components, padding=1)]
        if 'description' in self._question and self._question['description']:
            hsplit_components.insert(
                0,
                Label(
                    self._question['description'],
                    style='class:input.question',
                ),
            )
        return HSplit(hsplit_components, padding=1)

    def get_value(self):
        return self.get_widget().value


@register('date')
class DateHandler(QHandler):

    def get_widget_class(self):
        return MaskedInput

    def get_widget_init_kwargs(self):
        kwargs = dict(
            style='class:input.answer',
            mask='____-__-__',
            allowed_chars=string.digits,
        )
        return kwargs

    def get_layout(self):
        widget = self.get_widget()
        vsplit_components = [widget]
        if 'message' in self._question and self._question['message']:
            vsplit_components.insert(
                0,
                Label(
                    self._question['message'],
                    dont_extend_width=True,
                    style='class:input.question',
                ),
            )
        hsplit_components = [VSplit(vsplit_components, padding=1)]
        if 'description' in self._question and self._question['description']:
            hsplit_components.insert(
                0,
                Label(
                    self._question['description'],
                    style='class:input.question',
                ),
            )
        return HSplit(hsplit_components, padding=1)

    def get_value(self):
        return self.get_widget().value


@register('daterange')
class DateRangeHandler(QHandler):

    def get_widget_class(self):
        return DateRange

    def get_widget_init_kwargs(self):
        kwargs = dict(
            style='class:input.answer',
        )
        if 'from_label' in self._question:
            kwargs['from_label'] = self._question['from_label']
        if 'to_label' in self._question:
            kwargs['to_label'] = self._question['to_label']
        return kwargs

    def get_layout(self):
        widget = self.get_widget()
        vsplit_components = [widget]
        if 'message' in self._question and self._question['message']:
            vsplit_components.insert(
                0,
                Label(
                    self._question['message'],
                    dont_extend_width=True,
                    dont_extend_height=False,
                    style='class:input.question',
                ),
            )
        hsplit_components = [VSplit(vsplit_components, padding=1)]
        if 'description' in self._question and self._question['description']:
            hsplit_components.insert(
                0,
                Label(
                    self._question['description'],
                    style='class:input.question',
                ),
            )
        return HSplit(hsplit_components, padding=1)

    def get_value(self):
        return self.get_widget().value

    def get_formatted_value(self):
        value = self.get_value()
        return f'{value["from"]} - {value["to"]}'

    def get_keybindings(self):

        bindings = super().get_keybindings()

        @bindings.add(Keys.Tab)
        def _tab(event):
            get_app().layout.focus_next()

        @bindings.add(Keys.BackTab)
        def _s_tab(event):
            get_app().layout.focus_previous()

        return bindings
