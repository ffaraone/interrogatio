from .core.constants import InputMode
from .core.registries import (get_input_handlers_registry,
                              get_validators_registry)
from .dialog import dialogus
from .handlers import *
from .prompt import interrogatio
from .themes import DefaultTheme, get_theme_manager
from .validators import *

__version__ = '1.0.0b8'

__version_info__ = tuple([int(num) if num.isdigit() else num for num in __version__.replace('-', '.', 1).split('.')])


def get_version():
    return __version__





get_input_handlers_registry().register(ValueHandler)
get_input_handlers_registry().register(PasswordHandler)
get_input_handlers_registry().register(SelectOneHandler)
get_input_handlers_registry().register(SelectManyHandler)
get_input_handlers_registry().register(TextHandler)



get_validators_registry().register(RequiredValidator)
get_validators_registry().register(RegexValidator)
get_validators_registry().register(URLValidator)
get_validators_registry().register(EmailValidator)
get_validators_registry().register(MinLengthValidator)
get_validators_registry().register(MaxLengthValidator)
get_validators_registry().register(ExactLengthValidator)
get_validators_registry().register(NumberValidator)
get_validators_registry().register(IntegerValidator)
get_validators_registry().register(IPv4Validator)
get_validators_registry().register(RangeValidator)
get_validators_registry().register(MinValidator)
get_validators_registry().register(MaxValidator)


get_theme_manager().set_current_theme(DefaultTheme())
