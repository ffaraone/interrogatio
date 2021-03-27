import pytest

from interrogatio.handlers.base import _registry


@pytest.fixture
def registry():
    yield _registry
    _registry.clear()
