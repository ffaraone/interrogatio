import string

from prompt_toolkit.application import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import HSplit, VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.mouse_events import MouseEventType
from prompt_toolkit.widgets import Label, TextArea


class SelectOne(object):
    def __init__(  # noqa: CCR001
        self, values=None, default=None,
        accept_handler=None, style='',
    ):

        self.values = values or []
        self.current_value = (
            values[0][0] if values and not callable(values) else None
        )
        self._selected_index = 0
        self.accept_handler = accept_handler
        if default:
            self.value = default
        # Key bindings.
        kb = KeyBindings()

        @kb.add('up')
        def _(event):
            if not self.values:
                return
            self._selected_index = max(0, self._selected_index - 1)

        @kb.add('down')
        def _(event):
            if not self.values:
                return
            self._selected_index = min(
                len(self.values) - 1, self._selected_index + 1)

        @kb.add('pageup')
        def _(event):
            if not self.values:
                return
            w = event.app.layout.current_window
            self._selected_index = max(
                0,
                self._selected_index - len(w.render_info.displayed_lines),
            )

        @kb.add('pagedown')
        def _(event):
            if not self.values:
                return
            w = event.app.layout.current_window
            self._selected_index = min(
                len(self.values) - 1,
                self._selected_index + len(w.render_info.displayed_lines),
            )

        @kb.add(' ')
        def _(event):
            if not self.values:
                return
            self.current_value = self.values[self._selected_index][0]

        @kb.add(Keys.Any)
        def _(event):
            if not self.values:
                return
            # We first check values after the selected value, then all values.
            for value in self.values[self._selected_index + 1:] + self.values:
                if value[1].startswith(event.data):
                    self._selected_index = self.values.index(value)
                    return

        # Control and window.
        self.control = FormattedTextControl(
            lambda: self._get_text_fragments(style),
            key_bindings=kb,
            focusable=True)

        self.window = Window(
            content=self.control,
            style='class:radio-list',
            right_margins=[ScrollbarMargin(display_arrows=True)],
            dont_extend_height=True)

    @property
    def value(self):
        return self.current_value

    @value.setter
    def value(self, value):
        for i in range(len(self.values)):
            if self.values[i][0] == value:
                self._selected_index = i
                self.current_value = self.values[i][0]
                break

    def _get_text_fragments(self, out_style):  # pragma: no cover
        def mouse_handler(mouse_event):
            """
            Set `_selected_index` and `current_value` according to the y
            position of the mouse click event.
            """
            if mouse_event.event_type == MouseEventType.MOUSE_UP:
                self._selected_index = mouse_event.position.y
                self.current_value = self.values[self._selected_index][0]

        result = []
        for i, value in enumerate(self.values):
            checked = (value[0] == self.current_value)
            selected = (i == self._selected_index)
            style = out_style
            if checked:
                style += ' class:radio-checked'
            if selected:
                style += ' class:radio-selected'

            result.append((style, '('))

            if selected:
                result.append(('[SetCursorPosition]', ''))

            if checked:
                result.append((style, '*'))
            else:
                result.append((style, ' '))

            result.append((style, ')'))
            result.append((out_style + ' class:radio', ' '))
            result.extend(
                to_formatted_text(value[1], style=out_style + ' class:radio'))
            result.append(('', '\n'))

        # Add mouse handler to all fragments.
        for i, fragment in enumerate(result):
            result[i] = (fragment[0], fragment[1], mouse_handler)

        if result:
            result.pop()  # Remove last newline.
        return result

    def __pt_container__(self):
        return self.window


class SelectMany(object):
    def __init__(  # noqa: CCR001
        self, values=None, default=None,
        accept_handler=None, style='',
    ):

        self.values = values
        self.checked = None
        self._selected_index = 0
        self.accept_handler = accept_handler

        self.value = default or set()

        # Key bindings.
        kb = KeyBindings()

        @kb.add('up')
        def _(event):
            if not self.values:
                return
            self._selected_index = max(0, self._selected_index - 1)

        @kb.add('down')
        def _(event):
            if not self.values:
                return
            self._selected_index = min(
                len(self.values) - 1, self._selected_index + 1)

        @kb.add('pageup')
        def _(event):
            if not self.values:
                return
            w = event.app.layout.current_window
            self._selected_index = max(
                0,
                self._selected_index - len(w.render_info.displayed_lines),
            )

        @kb.add('pagedown')
        def _(event):
            if not self.values:
                return
            w = event.app.layout.current_window
            self._selected_index = min(
                len(self.values) - 1,
                self._selected_index + len(w.render_info.displayed_lines),
            )

        @kb.add(' ')
        def _(event):
            if not self.values:
                return
            if self.values[self._selected_index][0] in self.checked:
                self.checked.remove(self.values[self._selected_index][0])
            else:
                self.checked.add(self.values[self._selected_index][0])

        @kb.add(Keys.Any)
        def _(event):
            if not self.values:
                return
            # We first check values after the selected value, then all values.
            for value in self.values[self._selected_index + 1:] + self.values:
                if value[1].startswith(event.data):
                    self._selected_index = self.values.index(value)
                    return

        # Control and window.
        self.control = FormattedTextControl(
            lambda: self._get_text_fragments(style),
            key_bindings=kb,
            focusable=True)

        self.window = Window(
            content=self.control,
            style='class:checkbox-list',
            right_margins=[ScrollbarMargin(display_arrows=True)],
            dont_extend_height=True)

        if default:
            self.value = default

    @property
    def value(self):
        return list(self.checked)

    @value.setter
    def value(self, value):
        self.checked = set(value)

    def select_all(self):
        for v in self.values:
            self.checked.add(v[0])

    def select_none(self):
        self.checked.clear()

    def _generate_fragments(self, out_style):
        result = []
        for i, value in enumerate(self.values):
            checked = (value[0] in self.checked)
            selected = (i == self._selected_index)
            style = out_style
            if checked:
                style += ' class:checkbox-checked'
            if selected:
                style += ' class:checkbox-selected'

            result.append((style, '['))

            if selected:
                result.append(('[SetCursorPosition]', ''))

            if checked:
                result.append((style, '*'))
            else:
                result.append((style, ' '))

            result.append((style, ']'))
            result.append((out_style + ' class:checkbox', ' '))
            result.extend(
                to_formatted_text(
                    value[1],
                    style=out_style + ' class:checkbox',
                ),
            )
            result.append(('', '\n'))
        return result

    def _get_text_fragments(self, out_style):  # pragma: no cover
        def mouse_handler(mouse_event):
            """
            Set `_selected_index` and `current_value` according to the y
            position of the mouse click event.
            """
            if mouse_event.event_type == MouseEventType.MOUSE_UP:
                self._selected_index = mouse_event.position.y
                if self.values[self._selected_index][0] in self.checked:
                    self.checked.remove(self.values[self._selected_index][0])
                else:
                    self.checked.add(self.values[self._selected_index][0])

        result = self._generate_fragments(out_style)
        # Add mouse handler to all fragments.
        for i, fragment in enumerate(result):
            result[i] = (fragment[0], fragment[1], mouse_handler)

        result.pop()  # Remove last newline.
        return result

    def __pt_container__(self):
        return self.window


class FixedLengthBuffer(Buffer):
    def __init__(self, **kwargs):
        self._max_length = kwargs.pop('max_length')
        self._allowed_chars = kwargs.pop('allowed_chars')
        self._widget = kwargs.pop('widget')
        super().__init__(**kwargs)

    def _is_input_allowed(self, data):
        if not self._allowed_chars:
            return True
        return all([char in self._allowed_chars for char in data])

    def insert_text(
        self,
        data,
        overwrite=False,
        move_cursor=True,
        fire_event=True,
    ):
        if len(self.document.text) + len(data) <= self._max_length:
            if self._is_input_allowed(data):
                super().insert_text(data, overwrite, move_cursor, fire_event)
        if self.cursor_position == self._max_length:
            self.cursor_position -= 1
            self._widget.go_next(self)

    def delete_before_cursor(self, count=1):
        if self.cursor_position == 0:
            self._widget.go_previous(self)
        if self.cursor_position == self._max_length - 1:
            self.cursor_right()
        return super().delete_before_cursor(count=count)


class FixedLengthTextArea(TextArea):

    def __init__(
        self,
        text='',
        width=None,
        height=None,
        max_length=None,
        allowed_chars=None,
        widget=None,
        style=None,
    ):

        self.max_length = max_length

        self.buffer = FixedLengthBuffer(
            document=Document(text, 0),
            multiline=False,
            max_length=max_length,
            widget=widget,
            allowed_chars=allowed_chars,
            accept_handler=None,
        )

        self.control = BufferControl(
            buffer=self.buffer,
            focusable=True,
            focus_on_click=True,
        )

        height = D.exact(1)

        self.window = Window(
            height=height,
            width=width,
            content=self.control,
            style=style,
            wrap_lines=False,
        )


class MaskedInput(VSplit):

    def __init__(
        self,
        mask,
        placeholder='_',
        style=None,
        default=None,
        allowed_chars=None,
    ):
        self._mask = mask
        self._placeholder = placeholder

        self._components = []
        self._fields = []

        size = 0
        for i in range(len(self._mask)):
            char = self._mask[i]
            if char == placeholder:
                size += 1
                continue
            if size > 0:
                widget = FixedLengthTextArea(
                    width=size,
                    max_length=size,
                    style=style,
                    allowed_chars=allowed_chars,
                    widget=self,
                )
                self._components.append(widget)
                self._fields.append(widget)
                size = 0
            self._components.append(Label(char, dont_extend_width=True))

        if size > 0:
            widget = FixedLengthTextArea(
                width=size,
                max_length=size,
                style=style,
                widget=self,
                allowed_chars=allowed_chars,
            )
            self._components.append(widget)
            self._fields.append(widget)
        self._components.append(Label(''))
        if default:
            self.value = default

        super().__init__(self._components)

    def go_previous(self, component):
        if self._fields[0].buffer == component:
            return
        get_app().layout.focus_previous()
        current = get_app().layout.current_buffer
        current.cursor_right()
        current.delete_before_cursor()

    def go_next(self, component):
        if self._fields[-1].buffer == component:
            return
        get_app().layout.focus_next()

    def _has_value(self):
        values = ''.join([
            cmp.text for cmp in self._components
            if isinstance(cmp, FixedLengthTextArea)
        ]).strip()
        return bool(values)

    def _build_value(self):
        if self._has_value():
            return ''.join([cmp.text for cmp in self._components])
        return None

    @property
    def value(self):
        return self._build_value()

    @value.setter
    def value(self, val):
        if len(val) != len(self._mask):
            raise ValueError('Invalid value length')
        pos = 0
        non_mask_chars = self._mask.replace(self._placeholder, '')
        for char in non_mask_chars:
            val = val.replace(char, '')
        for field in self._fields:
            field.text = val[pos:pos + field.max_length]
            pos += field.max_length


class DateRange(HSplit):

    def __init__(
        self,
        from_label='From: ',
        to_label='  to: ',
        style=None,
    ):

        self._from = MaskedInput(
            mask='____-__-__', allowed_chars=string.digits, style=style,
        )
        self._to = MaskedInput(
            mask='____-__-__', allowed_chars=string.digits, style=style,
        )

        components = []

        if from_label:
            components.append(VSplit([
                Label(from_label, dont_extend_width=True),
                self._from,
            ]))
        else:
            components.append(self._from)

        if to_label:
            components.append(
                VSplit([
                    Label(to_label, dont_extend_width=True),
                    self._to,
                ]),
            )
        else:
            components.append(self._to)

        super().__init__(components)

    @property
    def value(self):
        return {
            'from': self._from.value,
            'to': self._to.value,
        }

    @value.setter
    def value(self, val):
        if 'from' in val:
            self._from.value = val['from']

        if 'to' in val:
            self._to.value = val['to']
