from .base import get_handlers_registry, Mode
from ..validators import ValidationContext
from .cmdline import ValueHandler, PasswordHandler, SelectOneHandler, SelectManyHandler


get_handlers_registry().register(ValueHandler)
get_handlers_registry().register(PasswordHandler)
get_handlers_registry().register(SelectOneHandler)
get_handlers_registry().register(SelectManyHandler)
