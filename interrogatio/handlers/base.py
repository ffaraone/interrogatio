import abc

import six

from ..core.exceptions import AlreadyRegisteredError, ValidationError

__all__ = [
    'QHandler',
    'register',
    'get_instance',
    'get_registered'
]


class QHandlersRegistry(dict):
    def register(self, alias, clazz):
        if alias in self:
            raise AlreadyRegisteredError('alias {} already exists'.format(
                alias))
        self[alias] = clazz

    def get_registered(self):
        return list(self.keys())

    def get_instance(self, question):
        qtype = question['type']
        clazz = self[qtype]
        return clazz(question)

_registry = QHandlersRegistry()


def register(alias, clazz):
    _registry.register(alias, clazz)


def get_instance(question):
    return _registry.get_instance(question)


def get_registered():
    return _registry.get_registered()


class QHandler(six.with_metaclass(abc.ABCMeta, object)):
    """
    ABC for the different kinds of input handlers.
    """

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

    def get_init_extra_args(self):
        return self._question.get('extra_args', dict())

    @abc.abstractmethod
    def get_widget_class(self):
        pass

    def get_widget(self):
        if not self._widget:
            clazz = self.get_widget_class()
            self._widget = clazz(**self.get_widget_init_kwargs())
        return self._widget

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
