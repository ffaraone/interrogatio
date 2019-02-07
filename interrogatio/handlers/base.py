import abc

import six
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.shortcuts import print_formatted_text

from ..themes import get_current_theme
from ..validators import ValidationError


__all__ = [
    'registry',
    'Interrogatio'
]

class Interrogatio(six.with_metaclass(abc.ABCMeta, object)):

    def __init__(self, question, context):
        self._question = question
        self._context = context

    @abc.abstractmethod
    def get_kwargs(self):
        pass

    def apply_validators(self, answer):
        validators = self._question.get('validators', [])
        validation_results = []
        for validator in validators:
            try:
                validator.validate(answer, self._context)
                validation_results.append(True)
            except ValidationError as ve:
                print_formatted_text(
                    FormattedText([
                        ('class:interrogatio.error', ve.message)
                    ]),
                    style=get_current_theme()
                )
                validation_results.append(False)
        
        return all(validation_results)

    @abc.abstractmethod
    def get_app(self):
        pass

    def get_input(self):
        while True:
            answer = self.get_app().run()
            if self.apply_validators(answer):
                return answer



class Registry(dict):
    def register(self, name, clazz):
        self[name] = clazz


registry = Registry()
