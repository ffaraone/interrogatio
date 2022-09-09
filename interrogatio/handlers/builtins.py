# pylint: disable=unused-argument
import string
from datetime import date, datetime

import pytz
from prompt_toolkit.application.current import get_app
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import HSplit, VSplit
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.widgets import Box, Button, Label, TextArea
from tzlocal import get_localzone_name

from interrogatio.handlers.base import QHandler
from interrogatio.handlers.registry import register
from interrogatio.widgets import DateRange, MaskedInput, SelectMany, SelectOne


@register('input')
class StringHandler(QHandler):

    def get_widget_class(self):
        return TextArea

    def get_widget_init_kwargs(self):
        kwgars = dict(
            multiline=self._question.get('multiline', False),
            style='class:input.answer',
        )
        default = self.get_question().get('default')
        if default and not callable(default):
            kwgars['text'] = default
        return kwgars

    def set_context(self, context):
        widget = self.get_widget()
        default = self.get_question().get('default')
        if default and callable(default):
            widget.text = default(context)
            widget.buffer.cursor_position = len(widget.text)

    def get_layout(self):
        widget = self.get_widget()
        vsplit_components = [widget]
        widget.buffer.cursor_position = len(widget.text)
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
                Window(
                    FormattedTextControl(
                        FormattedText([(
                            'class:input.question',
                            self._question['description'],
                        )]),
                    ),
                    wrap_lines=True,
                    height=D(min=1, max=5, preferred=3),
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
        kwgars = dict(
            multiline=self._question.get('multiline', False),
            password=True,
            style='class:password.answer',
        )
        default = self.get_question().get('default')
        if default and not callable(default):
            kwgars['text'] = default
        return kwgars

    def set_context(self, context):
        widget = self.get_widget()
        default = self.get_question().get('default')
        if default and callable(default):
            widget.text = default(context)
            widget.buffer.cursor_position = len(widget.text)

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
                Window(
                    FormattedTextControl(
                        FormattedText([(
                            'class:password.question',
                            self._question['description'],
                        )]),
                    ),
                    wrap_lines=True,
                    height=D(min=1, max=5, preferred=3),
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
        values = self.get_question()['values']
        kwargs = dict(
            values=values if not callable(values) else None,
            style='class:selectone.answer',
        )
        default = self.get_question().get('default')
        if default and not callable(default):
            kwargs['default'] = default

        return kwargs

    def set_context(self, context):
        widget = self.get_widget()
        values = self.get_question()['values']
        if callable(values):
            values = values(context)
            widget.values = values or []
            widget.current_value = values[0][0] if values else None
        default = self.get_question().get('default')
        if default and callable(default):
            widget.value = default(context)

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
                Window(
                    FormattedTextControl(
                        FormattedText([(
                            'class:selectone.question',
                            self._question['description'],
                        )]),
                    ),
                    wrap_lines=True,
                    height=D(min=1, max=5, preferred=3),
                ),
            )
        return HSplit(hsplit_components, padding=1)

    def get_formatted_value(self):
        format = self._question.get(
            'formatting_template',
            '${label} (${value})',
        )
        value = self.get_value()
        options = {t[0]: t[1] for t in self._question['values']}
        return string.Template(format).safe_substitute(
            label=options[value], value=value,
        )


@register('selectmany')
class SelectManyHandler(QHandler):

    def get_widget_class(self):
        return SelectMany

    def get_value(self):
        return self.get_widget().value

    def get_widget_init_kwargs(self):
        values = self.get_question()['values']
        kwargs = dict(
            values=values if not callable(values) else None,
            style='class:selectmany.answer',
        )
        default = self.get_question().get('default')
        if default and not callable(default):
            kwargs['default'] = default

        return kwargs

    def set_context(self, context):
        widget = self.get_widget()
        values = self.get_question()['values']
        if callable(values):
            values = values(context)
            widget.values = values or []
        default = self.get_question().get('default')
        if default and callable(default):
            widget.value = default(context)

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
                Window(
                    FormattedTextControl(
                        FormattedText([(
                            'class:selectone.question',
                            self._question['description'],
                        )]),
                    ),
                    wrap_lines=True,
                    height=D(min=1, max=5, preferred=3),
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
        format = self._question.get(
            'formatting_template',
            '${label} (${value})',
        )
        values = self.get_value()
        if not values:
            return ''

        if callable(self._question['values']):
            options = {t[0]: t[1] for t in self.get_widget().values}
        else:
            options = {t[0]: t[1] for t in self._question['values']}

        formatted_values = []

        for idx, value in enumerate(values):
            if idx > 14:
                formatted_values.append('...')
                break
            formatted_values.append(
                string.Template(format).safe_substitute(
                    label=options[value], value=value,
                ),
            )

        return ', '.join(formatted_values)


@register('maskedinput')
class MaskedInputHandler(QHandler):

    def get_widget_class(self):
        return MaskedInput

    def get_widget_init_kwargs(self):
        mask = self.get_question()['mask']
        kwargs = dict(
            style='class:input.answer',
            mask=mask,
        )
        default = self.get_question().get('default')
        if default and not callable(default):
            kwargs['default'] = default

        return kwargs

    def set_context(self, context):
        widget = self.get_widget()
        default = self.get_question().get('default')
        if default and callable(default):
            widget.value = default(context)

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
                Window(
                    FormattedTextControl(
                        FormattedText([(
                            'class:input.question',
                            self._question['description'],
                        )]),
                    ),
                    wrap_lines=True,
                    height=D(min=1, max=5, preferred=3),
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
        default = self.get_question().get('default')
        if default and not callable(default):
            if isinstance(default, (date, datetime)):
                kwargs['default'] = default.strftime('%Y-%m-%d')
            else:
                kwargs['default'] = default
        return kwargs

    def set_context(self, context):
        widget = self.get_widget()
        default = self.get_question().get('default')
        if default and callable(default):
            value = default(context)
            if isinstance(value, (date, datetime)):
                widget.value = value.strftime('%Y-%m-%d')
            else:
                widget.value = value

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
                Window(
                    FormattedTextControl(
                        FormattedText([(
                            'class:input.question',
                            self._question['description'],
                        )]),
                    ),
                    wrap_lines=True,
                    height=D(min=1, max=5, preferred=3),
                ),
            )
        return HSplit(hsplit_components, padding=1)

    def to_python(self):
        value = self.get_value()
        if not value:
            return

        question = self.get_question()
        if 'timezone' in question:
            tzinfo = pytz.timezone(question['timezone'])
        else:
            tzinfo = pytz.timezone(get_localzone_name())

        year, month, day = value.split('-')
        return tzinfo.localize(
            datetime(int(year), int(month), int(day)),
        )

    def get_value(self):
        return self.get_widget().value


@register('daterange')
class DateRangeHandler(QHandler):

    def get_widget_class(self):
        return DateRange

    def get_widget_init_kwargs(self):  # noqa: CCR001
        kwargs = dict(
            style='class:input.answer',
        )
        if 'from_label' in self._question:
            kwargs['from_label'] = self._question['from_label']
        if 'to_label' in self._question:
            kwargs['to_label'] = self._question['to_label']
        default = self.get_question().get('default')
        if default and not callable(default):
            kwargs['default'] = {}
            default_from = default.get('from')
            if default_from:
                if isinstance(default_from, (date, datetime)):
                    kwargs['default']['from'] = default_from.strftime(
                        '%Y-%m-%d',
                    )
                else:
                    kwargs['default']['from'] = default_from
            default_to = default.get('to')
            if default_to:
                if isinstance(default_to, (date, datetime)):
                    kwargs['default']['to'] = default_to.strftime('%Y-%m-%d')
                else:
                    kwargs['default']['to'] = default_to
        return kwargs

    def set_context(self, context):
        widget = self.get_widget()
        default = self.get_question().get('default')
        if default and callable(default):
            value = default(context)
            default_value = {}
            default_from = value.get('from')
            if default_from:
                if isinstance(default_from, (date, datetime)):
                    default_value['from'] = default_from.strftime(
                        '%Y-%m-%d',
                    )
                else:
                    default_value['from'] = default_from
            default_to = value.get('to')
            if default_to:
                if isinstance(default_to, (date, datetime)):
                    default_value['to'] = default_to.strftime('%Y-%m-%d')
                else:
                    default_value['to'] = default_to
            widget.value = default_value

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
                Window(
                    FormattedTextControl(
                        FormattedText([(
                            'class:input.question',
                            self._question['description'],
                        )]),
                    ),
                    wrap_lines=True,
                    height=D(min=1, max=5, preferred=3),
                ),
            )
        return HSplit(hsplit_components, padding=1)

    def to_python(self):
        question = self.get_question()
        if 'timezone' in question:
            tzinfo = pytz.timezone(question['timezone'])
        else:
            tzinfo = pytz.timezone(get_localzone_name())

        from_date = None
        to_date = None

        value = self.get_value()

        from_value = value.get('from')
        if from_value:
            year, month, day = from_value.split('-')
            from_date = tzinfo.localize(
                datetime(int(year), int(month), int(day)),
            )

        to_value = value.get('to')
        if to_value:
            year, month, day = to_value.split('-')
            to_date = tzinfo.localize(datetime(int(year), int(month), int(day)))

        return {
            'from': from_date,
            'to': to_date,
        }

    def get_value(self):
        return self.get_widget().value

    def get_formatted_value(self):
        format = self._question.get(
            'formatting_template',
            'from ${start} - to ${end}',
        )
        value = self.get_value()
        return string.Template(format).safe_substitute(
            start=value['from'], end=value['to'],
        )

    def get_keybindings(self):

        bindings = super().get_keybindings()

        @bindings.add(Keys.Tab)
        def _tab(event):
            get_app().layout.focus_next()

        @bindings.add(Keys.BackTab)
        def _s_tab(event):
            get_app().layout.focus_previous()

        return bindings
