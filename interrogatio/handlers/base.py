from abc import ABCMeta, abstractmethod

from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys

from interrogatio.core.exceptions import ValidationError

__all__ = [
    'QHandler',
]


class QHandler(metaclass=ABCMeta):
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

    @abstractmethod
    def get_layout(self):
        """
        Returns the UI layout of the question. It must returns a
        python-prompt-toolkit layout container.

        Subclasses must implement this method.

        :return: the UI layout of the question.
        :rtype: :class:`~prompt_toolkit.layout.Layout`
        """
        raise NotImplementedError(
            'Subclass must implements `get_layout` method.',
        )

    def get_question(self):
        return self._question

    @abstractmethod
    def get_value(self):
        """
        Returns the ``value`` part of the answer.

        Subclasses must implement this method.

        :return: the ``value`` part of the answer.
        :rtype: str
        """
        raise NotImplementedError(
            'Subclass must implements `get_value` method.',
        )

    def get_formatted_value(self):
        return self.get_value()

    @abstractmethod
    def get_widget_init_kwargs(self):
        """
        Returns the keyword arguments needed to instantiate the widget.

        Subclasses must implement this method.

        :return: a dictionary containing the keyword arguments.
        :rtype: dict
        """
        raise NotImplementedError(
            'Subclass must implements `get_widget_init_kwargs` method.',
        )

    def get_init_extra_args(self):
        """
        Returns extra arguments needed to instantiate a QHandler.
        The extra arguments are represented as a dictionary within the
        question object under the key ``extra_args``.

        :return: a dictionary containing the initialization extra arguments.
        :rtype: dict
        """
        return self.get_question().get('extra_args', dict())

    @abstractmethod
    def get_widget_class(self):
        """
        Returns the widget class for this QHandler.

        :return: a widget class.
        :rtype: class
        """
        raise NotImplementedError(
            'Subclass must implements `get_widget_class` method.',
        )

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

    def get_keybindings(self):
        """
        Returns a KeyBindings object to add custom keybindings to this
        QHandler.
        """
        bindings = KeyBindings()

        @bindings.add(Keys.ControlC)
        def _ctrl_c(event):
            get_app().exit(result=False)

        @bindings.add(Keys.Enter)
        def _enter(event):
            get_app().exit(result=True)

        return bindings

    def to_python(self):
        return self.get_value()

    def get_answer(self):
        """
        Returns dictionary with the question variable as key and the answer
        as the value.
        """
        return {self.get_question()['name']: self.to_python()}

    def get_variable_name(self):
        """
        Returns the name of the variable of this question.
        """
        return self._question['name']

    def get_label(self):
        """
        Returns the label of the variable of this question.
        """
        return self._question.get(
            'label', self.get_variable_name().capitalize(),
        )

    def is_disabled(self, context=None):
        """
        If disabled flag specified, it is evaluated if needed and returned.
        By default, all questions are enabled.
        """
        disabled = self._question.get('disabled', False)
        if callable(disabled):
            return disabled(context)
        else:
            return disabled

    def is_valid(self, context=None):
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
                validator.validate(self.get_value(), context=context)
            except ValidationError as ve:
                self._errors.append(str(ve))
        return not self._errors
