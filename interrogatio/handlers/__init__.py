from .base import registry
from ..validators import ValidationContext
from .cmdline import ValueInterrogatio, PasswordInterrogatio, SelectOneInterrogatio


registry.register('input', ValueInterrogatio)
registry.register('password', PasswordInterrogatio)
registry.register('selectone', SelectOneInterrogatio)


def get_handler(question, questions, answers):
    qtype = question['type']
    clazz = registry[qtype]
    return clazz(question, ValidationContext(questions, answers))