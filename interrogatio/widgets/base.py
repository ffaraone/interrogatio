# pylint: disable=unused-argument
import string

from prompt_toolkit.application import get_app
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import Window, VSplit
from prompt_toolkit.layout.controls import FormattedTextControl, BufferControl
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.layout.processors import Processor
from prompt_toolkit.widgets import Label, TextArea
from prompt_toolkit.mouse_events import MouseEventType


class SelectOne(object):
    def __init__(self, values=None, default=None,
                 accept_handler=None, style=''):
        assert isinstance(values, list)
        assert all(isinstance(i, tuple) and len(i) == 2
                   for i in values)

        self.values = values or []
        self.current_value = values[0][0]
        self._selected_index = 0
        self.accept_handler = accept_handler

        for i in range(len(self.values)):
            if self.values[i][0] == default:
                self._selected_index = i
                self.current_value = self.values[i][0]
                break


        # Key bindings.
        kb = KeyBindings()

        @kb.add('up')
        def _(event):
            self._selected_index = max(0, self._selected_index - 1)

        @kb.add('down')
        def _(event):
            self._selected_index = min(
                len(self.values) - 1, self._selected_index + 1)

        @kb.add('pageup')
        def _(event):
            w = event.app.layout.current_window
            self._selected_index = max(
                0,
                self._selected_index - len(w.render_info.displayed_lines)
            )

        @kb.add('pagedown')
        def _(event):
            w = event.app.layout.current_window
            self._selected_index = min(
                len(self.values) - 1,
                self._selected_index + len(w.render_info.displayed_lines)
            )

        @kb.add(' ')
        def _(event):
            self.current_value = self.values[self._selected_index][0]

        @kb.add('enter')
        def _(event):
            if self.accept_handler:
                self.accept_handler(self.current_value)

        @kb.add(Keys.Any)
        def _(event):
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

    def _get_text_fragments(self, out_style):
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

        result.pop()  # Remove last newline.
        return result

    def __pt_container__(self):
        return self.window




class SelectMany(object):
    def __init__(self, values=None, checked=None, default=None,
                 accept_handler=None, style=''):
        assert isinstance(values, list)
        assert all(isinstance(i, tuple) and len(i) == 2
                   for i in values)

        self.values = values
        self.checked = checked or set()
        self._selected_index = 0
        self.accept_handler = accept_handler

        # for i in range(len(self.values)):
        #     if self.values[i][0] == default:
        #         self._selected_index = i
        #         self.current_value = self.values[i][0]
        #         break


        # Key bindings.
        kb = KeyBindings()

        @kb.add('up')
        def _(event):
            self._selected_index = max(0, self._selected_index - 1)

        @kb.add('down')
        def _(event):
            self._selected_index = min(
                len(self.values) - 1, self._selected_index + 1)

        @kb.add('pageup')
        def _(event):
            w = event.app.layout.current_window
            self._selected_index = max(
                0,
                self._selected_index - len(w.render_info.displayed_lines)
            )

        @kb.add('pagedown')
        def _(event):
            w = event.app.layout.current_window
            self._selected_index = min(
                len(self.values) - 1,
                self._selected_index + len(w.render_info.displayed_lines)
            )

        @kb.add(' ')
        def _(event):
            if self.values[self._selected_index][0] in self.checked:
                self.checked.remove(self.values[self._selected_index][0])
            else:
                self.checked.add(self.values[self._selected_index][0])


        @kb.add('enter')
        def _(event):
            if self.accept_handler:
                self.accept_handler(list(self.checked))

        @kb.add(Keys.Any)
        def _(event):
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

    def select_all(self):
        for v in self.values:
            self.checked.add(v[0])

    def select_none(self):
        self.checked.clear()

    def _get_text_fragments(self, out_style):
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
                to_formatted_text(value[1],
                                  style=out_style + ' class:checkbox'))
            result.append(('', '\n'))

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
        self._focus_next = kwargs.pop('focus_next')
        self._allowed_chars = kwargs.pop('allowed_chars')
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
            if self._focus_next:
                get_app().layout.focus_next()



class FixedLengthTextArea(TextArea):
 
    def __init__(
        self,
        text='',
        width=None,
        height=None,
        max_length=None,
        focus_next=True,
        allowed_chars=None,
        style=None,
    ):


        self.buffer = FixedLengthBuffer(
            document=Document(text, 0),
            multiline=False,
            max_length=max_length,
            focus_next=focus_next,
            allowed_chars=allowed_chars,
            accept_handler=None,
        )

        self.control = BufferControl(
            buffer=self.buffer,
            focusable=True,
            focus_on_click=True,
        )

        height = D.exact(1)
        left_margins = []
        right_margins = []

        # style = "class:text-area "

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
        value=None,
        allowed_chars=None,
        accept_handler=None,
    ):
        self._mask = mask
        self._placeholder = placeholder
        self._accept_handler = accept_handler
        self._value = value

        self.current_position = 0
        self._components = []

        # Key bindings.
        kb = KeyBindings()

        @kb.add('enter')
        def _(event):
            if self.accept_handler:
                self.accept_handler(self.value)

        size = 0
        for i in range(len(self._mask)):
            char = self._mask[i]
            if char == placeholder:
                size += 1
                continue
            not_latest_field = char in self._mask[i:]
            if size > 0:
                widget = FixedLengthTextArea(
                    width=size,
                    max_length=size,
                    style=style,
                    allowed_chars=allowed_chars,
                    focus_next=not_latest_field,
                )
                self._components.append(widget)
                size = 0
            self._components.append(Label(char, dont_extend_width=True))

        if size > 0:
            widget = FixedLengthTextArea(
                width=size,
                max_length=size,
                style=style,
                focus_next=False,
                allowed_chars=allowed_chars,
            )
            self._components.append(widget)       
        self._components.append(Label(''))

        super().__init__(self._components, key_bindings=kb)

    def _has_value(self):
        values = ''.join([
            cmp.text for cmp in self._components
            if isinstance(cmp, FixedLengthTextArea)
        ]).strip()
        return bool(values)

    @property
    def value(self):
        if self._has_value():
            return ''.join([cmp.text for cmp in self._components])
        return None



class DateRange(VSplit):

    def __init__(self, from_label='From: ', to_label='till: ', style=None):


        self._from = MaskedInput(mask='____-__-__', allowed_chars=string.digits, style=style)
        self._to = MaskedInput(mask='____-__-__', allowed_chars=string.digits, style=style)

        # Key bindings.
        kb = KeyBindings()

        @kb.add('enter')
        def _(event):
            if self.accept_handler:
                self.accept_handler(self.value)

        components = []
        if from_label:
            components.append(Label(from_label, dont_extend_width=True))
        components.append(self._from)

        if to_label:
            components.append(Label(to_label, dont_extend_width=True))
        
        components.append(self._to)

        super().__init__(components, key_bindings=kb)
    
    @property
    def value(self):
        return {
            'from': self._from.value,
            'to': self._to.value,
        }