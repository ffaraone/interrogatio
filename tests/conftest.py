import copy

import pytest
from prompt_toolkit.application import create_app_session
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput

from interrogatio.handlers.base import QHandler
from interrogatio.handlers.registry import (
    _registry as h_registry,
)
from interrogatio.validators.registry import _registry as v_registry


@pytest.fixture
def handlers_registry(mocker):
    registry_copy = copy.deepcopy(h_registry)
    registry_copy.clear()
    mocker.patch(
        "interrogatio.handlers.registry.get_registry",
        return_value=registry_copy,
    )
    yield registry_copy
    registry_copy.clear()


@pytest.fixture
def validators_registry(mocker):
    registry_copy = copy.deepcopy(v_registry)
    registry_copy.clear()
    mocker.patch(
        "interrogatio.validators.registry.get_registry",
        return_value=registry_copy,
    )
    yield registry_copy
    registry_copy.clear()


@pytest.fixture
def test_handler():
    class TestHandler(QHandler):
        def get_layout(self):
            pass

        def get_value(self):
            pass

        def get_widget_init_kwargs(self):
            pass

        def get_widget_class(self):
            pass

        def get_keybindings(self):
            pass

    return TestHandler


@pytest.fixture
def mock_input():
    with create_pipe_input() as pipe_input:
        try:
            with create_app_session(
                input=pipe_input,
                output=DummyOutput(),
            ):
                yield pipe_input
        finally:
            pipe_input.close()
