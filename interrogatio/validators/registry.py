from interrogatio.core.exceptions import AlreadyRegisteredError
from interrogatio.validators.base import Validator


class ValidatorsRegistry(dict):
    def register(self, alias, clazz):
        if alias in self:
            raise AlreadyRegisteredError(
                'validator `{}` already exists.'.format(alias))
        self[alias] = clazz

    def get_registered(self):
        return list(self.keys())

    def get_instance(self, v):
        clazz = self[v['name']]
        if 'args' in v:
            return clazz(**v['args'])
        return clazz()


_registry = ValidatorsRegistry()


def get_registry():
    return _registry


def register(name):
    if name in get_registry().get_registered():
        raise AlreadyRegisteredError(
            f'The validator `{name}` is already registered.',
        )

    def _wrapper(cls):
        if not issubclass(cls, Validator):
            raise ValueError(
                'The provided class must be a subclass of Validator.',
            )

        get_registry().register(name, cls)

        return cls
    return _wrapper


def get_registered():
    """
    Returns a list of registered Validators.

    :return: list of aliases of the registered Validators.
    :rtype: list
    """
    return get_registry().get_registered()


def get_instance(v):
    """
    Returns an instance of a concrete subclass of Validator.

    :param v: a validator definition object.
    :type v: dict

    :return: an instance of the corresponding Validator.
    :rtype: Validator subclass
    """
    return get_registry().get_instance(v)
