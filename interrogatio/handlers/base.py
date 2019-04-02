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
    """
    Register a question handler to use with interrogatio.
    Each question handler is identified by a unique alias.
    This alias is used in question definition (type) to invoke a specific
    handler.


    :param alias: a unique alias to indentify a question handler.
    :type alias: str

    :param clazz: a QHandler concrete implementation.
    :type clazz: class
    """
    _registry.register(alias, clazz)


def get_instance(question):
    """
    Returns an instance of a concrete subclass of QHandler initialized with
    a question. The subclass of QHandler is identified by the ``type`` field
    of the question.

    :param question: a question to handle.
    :type question: dict

    :return: an instance of the corresponding QHandler
    :rtype: QHandler subclass
    """
    return _registry.get_instance(question)


def get_registered():
    """
    Returns a list of registered QHandlers.

    :return: list of aliases of the registered QHandlers.
    :rtype: list
    """
    return _registry.get_registered()


class QHandler(six.with_metaclass(abc.ABCMeta, object)):
    """
    ABC for question handlers.
    Each question handler must subclass this class.
    """

    def __init__(self, question):
        self._question = question
        self._widget = None
        self._errors = []

    @property
    def errors(self):
        """
        This property holds a list of validation error messages.
        The list is filled after a call to the is_valid method.

        :return: list of error messages.
        :rtype: list
        """
        return self._errors

    @abc.abstractmethod
    def get_layout(self):
        """
        Returns the UI layout of the question. It must returns a
        python-prompt-toolkit layout container.

        Subclasses must implement this method.

        :return: the UI layout of the question.
        :rtype: :class:`~prompt_toolkit.layout.Layout`
        """


    @abc.abstractmethod
    def get_value(self):
        """
        Returns the ``value`` part of the answer.

        Subclasses must implement this method.

        :return: the ``value`` part of the answer.
        :rtype: str
        """

    @abc.abstractmethod
    def get_widget_init_kwargs(self):
        """
        Returns the keyword arguments needed to instantiate the widget.

        Subclasses must implement this method.

        :return: a dictionary containing the keyword arguments.
        :rtype: dict
        """

    def get_init_extra_args(self):
        """
        Returns extra arguments needed to instantiate a QHandler.
        The extra arguments are represented as a dictionary within the
        question object under the key ``extra_args``.

        :return: a dictionary containing the initialization extra arguments.
        :rtype: dict
        """
        return self._question.get('extra_args', dict())

    @abc.abstractmethod
    def get_widget_class(self):
        """
        Returns the widget class for this QHandler.

        :return: a widget class.
        :rtype: class
        """

    def get_widget(self):
        """
        Returns the widget instance for this QHandler.
        If the widget has not been already created, this method creates it
        before returns.
        """
        if not self._widget:
            clazz = self.get_widget_class()
            self._widget = clazz(**self.get_widget_init_kwargs())
        return self._widget

    @abc.abstractmethod
    def get_keybindings(self):
        """
        Returns a KeyBindings object to add custom keybindings to this
        QHandler.
        """

    def get_answer(self):
        """
        Returns dictionary with the question variable as key and the answer
        as the value.
        """
        return {self._question['name']: self.get_value()}

    def get_variable_name(self):
        """
        Returns the name of the variable of this question.
        """
        return self._question['name']

    def is_valid(self):
        """
        Apply any speficied validator to the answer and return True if the
        input is valid otherwise False.
        If the answer isn't valid, it also set the errors property to a list
        of error messages.
        """
        validators = self._question.get('validators', [])
        self._errors = []
        for validator in validators:
            try:
                validator.validate(self.get_value())
            except ValidationError as ve:
                self._errors.append(ve.message)
        return not self._errors
