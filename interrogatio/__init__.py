from pkg_resources import DistributionNotFound, get_distribution

from interrogatio.core.dialog import dialogus
from interrogatio.core.prompt import interrogatio

__all__ = ('dialogus', 'interrogatio')


try:
    __version__ = get_distribution('interrogatio').version
except DistributionNotFound:  # pragma: no cover
    __version__ = '0.0.0'


def get_version():
    return __version__
