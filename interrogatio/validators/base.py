import abc
import six


from ..core.exceptions import ValidationError, AlreadyRegisteredError


__all__ = [
    'Validator',
    'register',
    'get_registered',
    'get_instance'
]


class ValidatorsRegistry(dict):
    def register(self, alias, clazz):
        if alias in self:
            raise AlreadyRegisteredError('validator {} already registered'.format(alias))
        self[alias] = clazz
    
    
    def get_registered(self):
        return list(self.keys())

    def get_instance(self, v):
        clazz = self[v['name']]
        if 'args' in v:
            return clazz(**v['args'])
        return clazz()

_registry = ValidatorsRegistry()


def register(alias, clazz):
    _registry.register(alias, clazz)

def get_registered():
    return _registry.get_registered()

def get_instance(v):
    return _registry.get_instance(v)


class Validator(six.with_metaclass(abc.ABCMeta, object)):
    """
    Abstract class for validators. 

    .. note::  
        Subclasses must provide a ``ALIAS`` static member with the name 
        of the validator.
        Validator aliases must be unique.
    """
    def __init__(self, message='invalid input'):
        self.message = message

    @abc.abstractmethod
    def validate(self, value):
        """
        Abstract method.
        Subclasses must implement this method with the validation logic.

        :param value: the value to validate.
        :type value: str

        :raises: 
            ValidationError: if the provided input is invalid.
        """


