from .base import registry, InterrogatioMode
from ..validators import ValidationContext
from .cmdline import ValueInterrogatio, PasswordInterrogatio, SelectOneInterrogatio


registry.register('input', ValueInterrogatio)
registry.register('password', PasswordInterrogatio)
registry.register('selectone', SelectOneInterrogatio)


def get_handler(question, questions, answers, mode):
    qtype = question['type']
    clazz = registry[qtype]
    return clazz(question, ValidationContext(questions, answers), mode=mode)