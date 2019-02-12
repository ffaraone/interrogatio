from .base import (EmailValidator, ExactLengthValidator, IntegerValidator,
                   MaxLengthValidator, MinLengthValidator, NumberValidator,
                   RegexValidator, RequiredValidator, URLValidator,
                   get_validators_registry, ValidationContext, ValidationError, 
                   Validator)

get_validators_registry().register(RequiredValidator)
get_validators_registry().register(RegexValidator)
get_validators_registry().register(URLValidator)
get_validators_registry().register(EmailValidator)
get_validators_registry().register(MinLengthValidator)
get_validators_registry().register(MaxLengthValidator)
get_validators_registry().register(ExactLengthValidator)
get_validators_registry().register(NumberValidator)
get_validators_registry().register(IntegerValidator)
