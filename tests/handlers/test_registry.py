import pytest

from interrogatio.core.exceptions import AlreadyRegisteredError
from interrogatio.handlers.base import QHandler
from interrogatio.handlers.registry import (
    get_instance, get_registered, QHandlersRegistry, register,
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


def test_register(handlers_registry):

    @register('alias')
    class TestClass(QHandler):
        pass

    assert 'alias' in handlers_registry
    assert issubclass(handlers_registry['alias'], TestClass)


def test_register_already_registered(handlers_registry):

    @register('alias')
    class TestClass(QHandler):
        pass

    with pytest.raises(AlreadyRegisteredError) as cv:
        @register('alias')
        class TestClass2(QHandler):
            pass

    assert str(cv.value) == 'The handler `alias` is already registered.'


def test_get_registered(handlers_registry):
    registered = get_registered()

    assert isinstance(registered, list)
    assert len(registered) == 0

    @register('alias')
    class TestClass(QHandler):
        pass

    registered = get_registered()

    assert isinstance(registered, list)
    assert len(registered) == 1
    assert registered[0] == 'alias'


def test_get_instance(handlers_registry):

    @register('test')
    class TestClass(QHandler):
        def __init__(self, question):
            self.question = question

        def get_layout(self):
            pass

        def get_value(self):
            pass

        def get_widget_init_kwargs(self):
            pass

        def get_widget_class(self):
            pass

    question = {'type': 'test'}

    instance = get_instance(question)

    assert isinstance(instance, TestClass)
    assert instance.question == question
