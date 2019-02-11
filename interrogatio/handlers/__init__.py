from .base import get_registry, Mode
from ..validators import ValidationContext
from .cmdline import ValueHandler, PasswordHandler, SelectOneHandler, SelectManyHandler


get_registry().register(ValueHandler)
get_registry().register(PasswordHandler)
get_registry().register(SelectOneHandler)
get_registry().register(SelectManyHandler)


def get_handler(question, questions, answers, mode):
    qtype = question['type']
    clazz = get_registry()[qtype]
    return clazz(question, ValidationContext(questions, answers), mode=mode)