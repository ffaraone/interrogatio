from abc import ABCMeta, abstractmethod


__all__ = [
    'Validator',
]


class Validator(metaclass=ABCMeta):
    """
    Abstract class for validators.
    """
    def __init__(self, message='invalid input'):
        self.message = message

    @abstractmethod
    def validate(self, value, context=None):
        """
        Abstract method.
        Subclasses must implement this method with the validation logic.

        :param value: the value to validate.
        :type value: str

        :raises:
            ValidationError: if the provided input is invalid.
        """
