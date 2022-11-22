import string

from prompt_toolkit.application import get_app
from prompt_toolkit.filters import has_focus
from prompt_toolkit.formatted_text import FormattedText, HTML, to_formatted_text
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import (
    DynamicContainer,
    HorizontalAlign,
    HSplit,
    VSplit,
    Window,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.widgets import Box, Button, Frame, Label, Shadow


class WizardDialog:
    def __init__(  # noqa: CCR001
        self, title, handlers, intro=None, summary=False,
        next_text='Next', previous_text='Previous',
        cancel_text='Cancel', finish_text='Finish',
        fast_forward=False,
    ):
        self.title = title
        self.handlers = handlers
        self.answers = {}
        self.intro = intro
        self.summary = summary
        self.steps = []
        self.current_step_idx = 0
        self.title = title
        self.process_steps()
        self.current_step = self.steps[self.current_step_idx]
        self.label_next = next_text
        self.label_previous = previous_text
        self.label_cancel = cancel_text
        self.label_finish = finish_text
        self.error_messages = ''

        self.cancel_btn = Button(
            text=self.label_cancel,
            handler=self.cancel,
        )
        self.previous_btn = Button(
            text=self.label_previous,
            handler=self.previous,
        )
        self.next_btn = Button(
            text=self.label_next if len(self.steps) > 1 else self.label_finish,
            handler=self.next,
        )

        self.buttons = [self.next_btn, self.cancel_btn]

        if fast_forward:
            self.fast_forward()

        self.buttons_kb = KeyBindings()
        first_selected = has_focus(self.buttons[0])
        last_selected = has_focus(self.buttons[-1])

        self.buttons_kb.add('left', filter=~first_selected)(focus_previous)
        self.buttons_kb.add('right', filter=~last_selected)(focus_next)

        input_container = HSplit(
            [
                Box(
                    body=DynamicContainer(self.get_current_step_container),
                    padding=D(preferred=1, max=1),
                    padding_bottom=0,
                ),
            ],
        )

        left_container = Box(
            body=DynamicContainer(self.get_steps_labels),
            padding=D(preferred=1, max=1),
            padding_bottom=0,
        )
        right_container = HSplit(
            [
                input_container,
                Box(
                    body=DynamicContainer(self.get_status),
                    padding=D(preferred=1, max=1),
                    padding_bottom=1,
                ),
            ],
        )
        top_container = VSplit(
            [left_container, right_container],
            padding_char='│',
            padding=1,
            padding_style='#000000',
            height=D(min=10, preferred=24),
        )

        buttons_container = Box(
            body=DynamicContainer(self.get_buttons_container),
            height=D(min=1, max=3, preferred=3),
        )

        kb = KeyBindings()
        kb.add(Keys.Tab)(focus_next)
        kb.add(Keys.BackTab)(focus_previous)

        frame = Shadow(
            body=Frame(
                title=self.get_title,
                body=HSplit(
                    [
                        top_container,
                        buttons_container,
                    ],
                    padding_char='─',
                    padding=1,
                    padding_style='#000000',
                ),
                style='class:dialog.body',
                key_bindings=kb,
                width=D(min=78, preferred=132),
            ),
        )
        self.container = Box(
            body=frame, style='class:dialog',
        )

    def get_title(self):
        return (
            f'{self.title} - {self.current_step_idx + 1} of {len(self.steps)}'
        )

    def _get_step_style(self, idx):
        if idx == self.current_step_idx:
            return 'class:dialog.step.current'

        if (
                self.steps[idx].get('handler')
                and self.steps[idx]['handler'].is_disabled(context=self.answers)
        ):
            return 'class:dialog.step.disabled'

        return 'class:dialog.step'

    def get_steps_labels(self):
        steps_labels = []
        for idx, step in enumerate(self.steps, start=1):
            label = f'{idx}. {step["label"]}'
            steps_labels.append(
                Window(
                    FormattedTextControl(
                        to_formatted_text(
                            label,
                            style=self._get_step_style(idx - 1),
                        ),
                    ),
                    height=1,
                ),
            )
        return HSplit(steps_labels, width=33)

    def get_status(self):
        if self.error_messages:
            return Window(
                FormattedTextControl(
                    FormattedText([('class:error', self.error_messages)]),
                ),
                height=1,
            )
        return Label('')

    def get_summary(self):
        if isinstance(self.summary, bool):
            text = '\n'.join(
                [
                    f'<b>{handler.get_variable_name().capitalize()}:'
                    f' </b>{handler.get_formatted_value()}'
                    for handler in self.handlers
                ],
            )
        elif callable(self.summary):
            data = {
                handler.get_variable_name(): {
                    'question': handler.get_question(),
                    'value': handler.get_value(),
                    'formatted_value': handler.get_formatted_value(),
                }
                for handler in self.handlers
            }
            text = self.summary(data)
        else:
            text = string.Template(self.summary).safe_substitute(
                {
                    handler.get_variable_name(): handler.get_formatted_value()
                    for handler in self.handlers
                },
            )
        return Window(
            FormattedTextControl(to_formatted_text(HTML(text))),
            wrap_lines=True,
        )

    def get_current_step_container(self):
        return self.current_step['layout']

    def get_buttons_container(self):
        return VSplit(
            self.buttons,
            padding=1,
            key_bindings=self.buttons_kb,
        )

    def process_steps(self):
        if self.intro:
            layout = Window(
                FormattedTextControl(to_formatted_text(HTML(self.intro))),
                wrap_lines=True,
            )
            self.steps.append(
                {
                    'layout': layout,
                    'label': 'Introduction',
                    'handler': None,
                },
            )

        for handler in self.handlers:
            layout = handler.get_layout()
            layout.align = HorizontalAlign.JUSTIFY
            self.steps.append(
                {
                    'layout': layout,
                    'label': handler.get_label(),
                    'handler': handler,
                },
            )

        if self.summary:
            layout = Box(
                body=DynamicContainer(self.get_summary),
                padding=D(preferred=1, max=1),
                padding_bottom=1,
            )
            self.steps.append(
                {
                    'layout': layout,
                    'label': 'Summary',
                    'handler': None,
                },
            )

    def _check_no_next_steps(self):
        idx = self.current_step_idx + 1
        while idx <= len(self.steps) - 1:
            next_step = self.steps[idx]
            next_handler = next_step['handler']
            if next_handler and not next_handler.is_disabled(self.answers):
                return False
            idx += 1

        return True

    def set_buttons_labels(self):
        if len(self.steps) == 1:
            return

        if self.current_step_idx == 0:
            self.next_btn.text = self.label_next
            self.buttons = [self.next_btn, self.cancel_btn]
            return

        if (
            self.current_step_idx == len(self.steps) - 1
            or (self._check_no_next_steps() and not self.summary)
        ):
            self.next_btn.text = self.label_finish
        else:
            self.next_btn.text = self.label_next

        self.buttons = [self.next_btn, self.previous_btn, self.cancel_btn]

    def cancel(self):
        get_app().exit(result=False)

    def previous(self):
        if self.current_step_idx != 0:
            self.error_messages = ''
            self.current_step_idx -= 1
            self.current_step = self.steps[self.current_step_idx]
            handler = self.current_step['handler']
            if handler and handler.is_disabled(self.answers):
                return self.previous()
            get_app().layout.focus(self.current_step['layout'])

        self.set_buttons_labels()

    def next(self):  # noqa: CCR001
        if self.validate():
            if self.current_step_idx < len(self.steps) - 1:
                handler = self.current_step['handler']
                if handler:
                    self.answers.update(handler.get_answer())
                self.current_step_idx += 1
                self.current_step = self.steps[self.current_step_idx]
                handler = self.current_step['handler']
                if handler:
                    if handler.is_disabled(context=self.answers):
                        return self.next()  # noqa: B305
                    handler.set_context(self.answers)
                if not self.summary or self.current_step != self.steps[-1]:
                    get_app().layout.focus(self.current_step['layout'])
            else:
                get_app().exit(result=True)

        self.set_buttons_labels()

    def fast_forward(self):
        while self.current_step_idx < len(self.steps) - 1:
            if self.validate():
                step = self.steps[self.current_step_idx]
                handler = step['handler']
                if handler and not handler.is_disabled(self.answers):
                    self.answers.update(handler.get_answer())
                    handler.set_context(self.answers)
                self.current_step_idx += 1
            else:
                break

        self.current_step = self.steps[self.current_step_idx]
        self.set_buttons_labels()

    def validate(self):
        step = self.steps[self.current_step_idx]
        handler = step['handler']
        if (
                handler
                and not handler.is_valid(self.answers)
                and not handler.is_disabled(self.answers)
        ):
            self.error_messages = ','.join(handler.errors)
            return False
        self.error_messages = ''
        return True

    def __pt_container__(self):  # pragma: no cover
        return self.container
