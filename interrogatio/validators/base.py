import abc
import collections
import six



ValidationContext = collections.namedtuple(
    'ValidationContext', ['questions', 'answers'])

class ValidationError(Exception):
    def __init__(self, message):
        self._message = message
    
    def __str__(self):
        return self._message

    @property
    def message(self):
        return self._message


class Validator(six.with_metaclass(abc.ABCMeta, object)):

    def __init__(self, message='invalid input'):
        self.message = message

    @abc.abstractmethod
    def validate(self, value, context):
        if not isinstance(context, ValidationContext):
            raise ValueError('context must be a ValidationContext instance')
