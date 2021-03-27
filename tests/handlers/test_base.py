import pytest

from interrogatio.core.exceptions import AlreadyRegisteredError
from interrogatio.handlers.base import (
    QHandlersRegistry,
    get_instance,
    get_registered,
    register,
)


def test_registry_register():
    reg = QHandlersRegistry()

    class TestClass:
        pass

    reg.register('alias', TestClass)

    assert 'alias' in reg
    assert issubclass(reg['alias'], TestClass)


def test_registry_register_already_registered():
    reg = QHandlersRegistry()

    class TestClass:
        pass

    reg.register('alias', TestClass)
    with pytest.raises(AlreadyRegisteredError) as cv:
        reg.register('alias', TestClass)

    assert str(cv.value) == 'alias `alias` already exists.'


def test_registry_get_registered():
    reg = QHandlersRegistry()

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
    reg = QHandlersRegistry()

    class TestClass:
        def __init__(self, question):
            self.question = question

    reg.register('test', TestClass)

    question = {'type': 'test'}

    instance = reg.get_instance(question)

    assert isinstance(instance, TestClass)
    assert instance.question == question


def test_register(registry):
    class TestClass:
        pass

    register('alias', TestClass)

    assert 'alias' in registry
    assert issubclass(registry['alias'], TestClass)


def test_register_already_registered(registry):
    class TestClass:
        pass

    register('alias', TestClass)
    with pytest.raises(AlreadyRegisteredError) as cv:
        register('alias', TestClass)

    assert str(cv.value) == 'alias `alias` already exists.'


def test_get_registered(registry):
    registered = get_registered()

    assert isinstance(registered, list)
    assert len(registered) == 0

    class TestClass:
        pass

    register('alias', TestClass)

    registered = get_registered()

    assert isinstance(registered, list)
    assert len(registered) == 1
    assert registered[0] == 'alias'


def test_get_instance(registry):

    class TestClass:
        def __init__(self, question):
            self.question = question

    register('test', TestClass)

    question = {'type': 'test'}

    instance = get_instance(question)

    assert isinstance(instance, TestClass)
    assert instance.question == question
