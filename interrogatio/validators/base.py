import abc
import six


from ..core.exceptions import AlreadyRegisteredError


__all__ = [
    'Validator',
    'register',
    'get_registered',
    'get_instance'
]


class ValidatorsRegistry(dict):
    def register(self, alias, clazz):
        if alias in self:
            raise AlreadyRegisteredError(
                'validator {} already registered'.format(alias))
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
    """
    Register a validator to use with interrogatio.
    Each validator is identified by a unique alias.
    This alias can be used in question definition to validater answers.


    :param alias: a unique alias to indentify a validator.
    :type alias: str

    :param clazz: a Validator concrete implementation.
    :type clazz: class
    """
    _registry.register(alias, clazz)

def get_registered():
    """
    Returns a list of registered Validators.

    :return: list of aliases of the registered Validators.
    :rtype: list
    """
    return _registry.get_registered()

def get_instance(v):
    """
    Returns an instance of a concrete subclass of Validator.

    :param v: a validator definition object.
    :type v: dict

    :return: an instance of the corresponding Validator.
    :rtype: Validator subclass
    """
    return _registry.get_instance(v)


class Validator(six.with_metaclass(abc.ABCMeta, object)):
    """
    Abstract class for validators.
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
