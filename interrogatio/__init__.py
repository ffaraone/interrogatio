import pkg_resources

from .dialog import dialogus
from .prompt import interrogatio

__all__ = ('dialogus', 'interrogatio')

__version__ = pkg_resources.get_distribution('interrogatio').version

__version_info__ = tuple(
    [int(num) if num.isdigit() else
     num for num in __version__.replace('-', '.', 1).split('.')])
