import abc

import six
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import print_formatted_text

from ..core.constants import InputMode
from ..core.validation import ValidationContext
from ..themes import get_theme_manager
from ..validators import ValidationError

__all__ = [
    'QHandler'
]


# class QContext:
#     def __init__(self, question, questions, is_dialog=False):
#         self._question = question
#         self._questions = questions
#         self._is_dialog = is_dialog

#     @property
#     def question(self):
#         return self._question

#     @property
#     def questions(self):
#         return self._questions

#     @property
#     def is_dialog(self):
#         return self._is_dialog


class QHandler(six.with_metaclass(abc.ABCMeta, object)):
    """
    ABC for the different kinds of input handlers.
    """

    widget_class = None

    def __init__(self, question):
        self._question = question
        self._widget = None
        self._errors = []


    @property
    def errors(self):
        return self._errors

    @abc.abstractmethod
    def get_layout(self):
        pass

    @abc.abstractmethod
    def get_value(self):
        pass

    @abc.abstractmethod
    def get_widget_init_kwargs(self):
        pass

    def get_widget_class(self):
        return self.widget_class


    @abc.abstractmethod
    def get_keybindings(self):
        pass

    def get_answer(self):
        return {self._question['name']: self.get_value()}

    def get_variable_name(self):
        return self._question['name']

    def is_valid(self):
        """
        This method will be called by the get_input method to apply validators.
        """
        validators = self._question.get('validators', [])
        self._errors = []
        for validator in validators:
            try:
                validator.validate(self.get_value())
            except ValidationError as ve:
                self._errors.append(ve.message)
        return not self._errors

