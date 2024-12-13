from importlib_metadata import version

from interrogatio.core.dialog import dialogus
from interrogatio.core.prompt import interrogatio

__all__ = ("dialogus", "interrogatio")


__version__ = version("interrogatio")


def get_version():
    return __version__
