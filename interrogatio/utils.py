from .core.exceptions import InvalidQuestionError
from . import validators
from . import handlers


def _validate_validator_object(obj):
    if 'name' not in obj:
        raise InvalidQuestionError(
            'You must specify a name for the validator')

    if obj['name'] not in validators.get_registered():
        raise InvalidQuestionError(
            'Validator {} does not exists'.format(obj['name']))

    if 'args' in obj and not isinstance(obj['args'], dict):
        raise InvalidQuestionError('Validator arguments must be a dictionary')


def _validate_question(q):

    if 'name' not in q:
        raise InvalidQuestionError('You must specify a name for the question')

    if 'type' not in q:
        raise InvalidQuestionError('You must specify a question type')

    q_type = q['type']
    if q_type not in handlers.get_registered():
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

        validator_instances = []
        for v in q['validators']:
            if not isinstance(v, (validators.Validator, dict)):
                raise InvalidQuestionError(
                    'Validators must be a list of  '
                    'interrogatio.validators.Validator'
                    ' instances or a list of validator objects')

            if isinstance(v, dict):
                _validate_validator_object(v)
                v = validators.get_instance(v)
                validator_instances.append(v)
            else:
                validator_instances.append(v)
        q['validators'] = validator_instances


def validate_questions(questions):
    for q in questions:
        _validate_question(q)
