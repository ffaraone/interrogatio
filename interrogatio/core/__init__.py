from .base import interrogatio
from .utils import validate_question, InvalidQuestionError
from ..utils.registries import get_input_handlers_registry, get_validators_registry
from ..handlers import *
from ..validators import *
from ..themes import get_theme_manager, DefaultTheme

get_input_handlers_registry().register(ValueHandler)
get_input_handlers_registry().register(PasswordHandler)
get_input_handlers_registry().register(SelectOneHandler)
get_input_handlers_registry().register(SelectManyHandler)



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