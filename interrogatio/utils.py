from .exceptions import InvalidQuestionError
from .core.registries import get_input_handlers_registry, get_validators_registry
from .validators import Validator

def _validate_validator_object(obj):
    if 'name' not in obj:
        raise InvalidQuestionError('You must specify a name for the validator')    
    
    if obj['name'] not in get_validators_registry():
        raise InvalidQuestionError('Validator {} does not exists'.format(obj['name']))
    
    if 'args' in obj and not isinstance(obj['args'], dict):
        raise InvalidQuestionError('Validator arguments must be a dictionary')    
    
def _validate_question(q):

    if 'name' not in q:
        raise InvalidQuestionError('You must specify a name for the question')

    if 'message' not in q:
        raise InvalidQuestionError('You must specify a message for the question')
    
    if 'type' not in q:
        raise InvalidQuestionError('You must specify a question type')

    q_type = q['type']
    if q_type not in get_input_handlers_registry().get_registered():
        raise InvalidQuestionError('Unsupported question type: {}'.format(
            q_type))

    if q_type == 'selectone':
        if 'values' not in q:
            raise InvalidQuestionError('You must specify at least one '
                                       'choice for type choice')
        values = q['values']
        if not values:
            raise InvalidQuestionError('You must specify at least one '
                                       'choice for type choice')
        if not isinstance(values, (list, tuple)):
            raise InvalidQuestionError('Choices must be a list or tuple of'
                                       ' tuples.')
        first_value = values[0]
        if not isinstance(first_value, (list, tuple)):
            raise InvalidQuestionError('Choices must be a list or tuple of'
                                       ' tuples.')
        if len(first_value) != 2:
            raise InvalidQuestionError('Every choice must be a tuple'
                                       ' (value, label)')            

    if 'validators' in q:
        if not isinstance(q['validators'], (list, tuple)):
            raise InvalidQuestionError('Validators must be a list or tuple') 

        validators = []
        for v in q['validators']:
            if not isinstance(v, (Validator, dict)):
                raise InvalidQuestionError('Validators must be a list of  '
                    'interrogatio.validators.Validator'
                    ' instances or a list of validator objects')

            if isinstance(v, dict):
                _validate_validator_object(v)
                v = get_validators_registry().get_instance(v)
                validators.append(v)
            else:
                validators.append(v)
        q['validators'] = validators

def validate_questions(questions):
    for q in questions:
        _validate_question(q)
