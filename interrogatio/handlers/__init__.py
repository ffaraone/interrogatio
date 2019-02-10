from .base import registry, Mode
from ..validators import ValidationContext
from .cmdline import ValueHandler, PasswordHandler, SelectOneHandler


registry.register(ValueHandler)
registry.register(PasswordHandler)
registry.register(SelectOneHandler)


def get_handler(question, questions, answers, mode):
    qtype = question['type']
    clazz = registry[qtype]
    return clazz(question, ValidationContext(questions, answers), mode=mode)