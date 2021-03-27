import pytest

from interrogatio.core.exceptions import AlreadyRegisteredError
from interrogatio.validators.base import Validator
from interrogatio.validators.registry import (
    get_instance,
    get_registered,
    register,
    ValidatorsRegistry,
)


def test_registry_register():
    reg = ValidatorsRegistry()

    class TestClass:
        pass

    reg.register('alias', TestClass)

    assert 'alias' in reg
    assert issubclass(reg['alias'], TestClass)


def test_registry_register_already_registered():
    reg = ValidatorsRegistry()

    class TestClass:
        pass

    reg.register('alias', TestClass)
    with pytest.raises(AlreadyRegisteredError) as cv:
        reg.register('alias', TestClass)

    assert str(cv.value) == 'validator `alias` already exists.'


def test_registry_get_registered():
    reg = ValidatorsRegistry()

    registered = reg.get_registered()

    assert isinstance(registered, list)
    assert len(registered) == 0

    class TestClass:
        pass

    reg.register('alias', TestClass)

    registered = reg.get_registered()

    assert isinstance(registered, list)
    assert len(registered) == 1
    assert registered[0] == 'alias'


def test_registry_get_instance():
    reg = ValidatorsRegistry()

    class TestClass(Validator):
        def __init__(self, message=None):
            self.message = message

        def validate(self, value):
            pass

    reg.register('test', TestClass)

    validator = {'name': 'test'}

    instance = reg.get_instance(validator)

    assert isinstance(instance, TestClass)


def test_register(validators_registry):

    @register('alias')
    class TestClass(Validator):
        def validate(self, value):
            pass

    assert 'alias' in validators_registry
    assert issubclass(validators_registry['alias'], TestClass)


def test_register_already_registered(validators_registry):

    @register('alias')
    class TestClass(Validator):
        def validate(self, value):
            pass

    with pytest.raises(AlreadyRegisteredError) as cv:
        @register('alias')
        class TestClass2(Validator):
            def validate(self, value):
                pass

    assert str(cv.value) == 'The validator `alias` is already registered.'


def test_get_registered(validators_registry):
    registered = get_registered()

    assert isinstance(registered, list)
    assert len(registered) == 0

    @register('alias')
    class TestClass(Validator):
        def validate(self, value):
            pass

    registered = get_registered()

    assert isinstance(registered, list)
    assert len(registered) == 1
    assert registered[0] == 'alias'


@pytest.mark.parametrize('args', ({}, {'message': 'message'}))
def test_get_instance(validators_registry, args):

    @register('test')
    class TestClass(Validator):
        def __init__(self, message=None):
            self.message = message

        def validate(self, value):
            pass

    validator = {'name': 'test', 'args': args}
    instance = get_instance(validator)

    assert isinstance(instance, TestClass)
