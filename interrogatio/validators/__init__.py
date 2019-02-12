from .base import (EmailValidator, ExactLengthValidator, IntegerValidator,
                   IPv4Validator, MaxLengthValidator, MaxValidator,
                   MinLengthValidator, MinValidator, NumberValidator,
                   RangeValidator, RegexValidator, RequiredValidator,
                   URLValidator, ValidationContext, ValidationError, Validator,
                   get_validators_registry)

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
