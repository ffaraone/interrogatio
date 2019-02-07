from .handlers import get_handler
from .validators import Validator


__all__ = [
    'InvalidQuestionError',
    'interrogatio'
]


_QUESTION_TYPES = [
    'selectone',
    'input',
    'password',
    'repassword',
    'multiple',
    'text'
]


class InvalidQuestionError(Exception):
    pass


def _validate_question(q):

    if 'name' not in q:
        raise InvalidQuestionError('You must specify a name for the question')

    if 'message' not in q:
        raise InvalidQuestionError('You must specify a message for the question')
    
    if 'type' not in q:
        raise InvalidQuestionError('You must specify a question type')

    q_type = q['type']
    if q_type not in _QUESTION_TYPES:
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

        for v in q['validators']:
            if not isinstance(v, Validator):
                raise InvalidQuestionError('Validators must subclass '
                                           'interrogatio.validators.Validator') 

def interrogatio(questions):
    answers = {}
    for q in questions:
        _validate_question(q)
        answers[q['name']] = get_handler(q, questions, answers).get_input()
    return answers