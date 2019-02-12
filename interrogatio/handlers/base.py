import abc

import six
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import print_formatted_text

from ..themes import get_theme_manager
from ..utils.constants import InputMode
from ..validators import ValidationError
from ..utils.validation import ValidationContext


__all__ = [
    'InputHandler'
]


class InputHandler(six.with_metaclass(abc.ABCMeta, object)):

    def __init__(self, question, context, mode):
        self._question = question
        self._context = context
        self._mode = mode

    @abc.abstractstaticmethod
    def get_style_rules_names():
        pass

    @abc.abstractstaticmethod
    def get_style(mode, rules):
        pass

    @abc.abstractmethod
    def get_layout(self):
        pass

    @abc.abstractmethod
    def get_app(self):
        pass

    @abc.abstractmethod
    def get_value(self):
        pass

    @abc.abstractmethod
    def get_kwargs(self):
        pass

    def get_answer(self):
        return {self._question['name']: self.get_value()}

    def get_variable_name(self):
        return self._question['name']

    def apply_validators(self):
        validators = self._question.get('validators', [])
        error_messages = []
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

    def get_input(self):
        while True:
            answer = self.get_app().run()
            if not self.apply_validators():
                return answer

