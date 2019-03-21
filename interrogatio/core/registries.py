from ..core.validation import ValidationContext

__all__ = [
    'get_input_handlers_registry',
    'get_validators_registry'
]

class InputHandlersRegistry(dict):
    def register(self, clazz):
        self[clazz.ALIAS] = clazz
    
    def is_registered(self, alias):
        return alias in self
    
    def get_registered(self):
        return list(self.keys())

    def get_instance(self, question, questions, answers, mode):
        qtype = question['type']
        clazz = self[qtype]
        return clazz(
            question,
            ValidationContext(questions, answers),
            mode=mode)

_input_handlers_registry = InputHandlersRegistry()

def get_input_handlers_registry():
    return _input_handlers_registry



class ValidatorsRegistry(dict):
    def register(self, clazz):
        self[clazz.ALIAS] = clazz
    
    def is_registered(self, alias):
        return alias in self
    
    def get_registered(self):
        return list(self.keys())

    def get_instance(self, v):
        clazz = self[v['name']]
        if 'args' in v:
            return clazz(**v['args'])
        return clazz()

_validators_registry = ValidatorsRegistry()

def get_validators_registry():
    return _validators_registry