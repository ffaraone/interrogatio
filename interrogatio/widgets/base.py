from prompt_toolkit.application.current import get_app
from prompt_toolkit.formatted_text import to_formatted_text
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.mouse_events import MouseEventType


class SelectOne(object):
    def __init__(self, values=[], default=None, accept_handler=None, style=''):
        assert isinstance(values, list)
        assert len(values) > 0
        assert all(isinstance(i, tuple) and len(i) == 2
                   for i in values)

        self.values = values
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
            right_margins=[],
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
            result.extend(to_formatted_text(value[1], style=out_style + ' class:radio'))
            result.append(('', '\n'))

        # Add mouse handler to all fragments.
        for i in range(len(result)):
            result[i] = (result[i][0], result[i][1], mouse_handler)

        result.pop()  # Remove last newline.
        return result

    def __pt_container__(self):
        return self.window



class SelectMany(object):
    def __init__(self, values=[], checked=[], default=None, accept_handler=None, style=''):
        assert isinstance(values, list)
        assert len(values) > 0
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
            right_margins=[],
            dont_extend_height=True)

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
            result.extend(to_formatted_text(value[1], style=out_style + ' class:checkbox'))
            result.append(('', '\n'))

        # Add mouse handler to all fragments.
        for i in range(len(result)):
            result[i] = (result[i][0], result[i][1], mouse_handler)

        result.pop()  # Remove last newline.
        return result

    def __pt_container__(self):
        return self.window
