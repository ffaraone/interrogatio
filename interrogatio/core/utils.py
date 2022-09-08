from interrogatio import handlers, validators
from interrogatio.core.exceptions import InvalidQuestionError


def _validate_validator_object(obj):
    if 'name' not in obj:
        raise InvalidQuestionError(
            'You must specify a name for the validator.')

    if obj['name'] not in validators.get_registered():
        raise InvalidQuestionError(
            f'Validator {obj["name"]} does not exists.',
        )

    if 'args' in obj and not isinstance(obj['args'], dict):
        raise InvalidQuestionError('Validator arguments must be a dictionary.')


def _validate_question(q):  # noqa: CCR001

    if 'name' not in q:
        raise InvalidQuestionError('You must specify a name for the question.')

    if 'type' not in q:
        raise InvalidQuestionError('You must specify a question type.')

    q_type = q['type']
    if q_type not in handlers.get_registered():
        raise InvalidQuestionError(
            f'Unsupported question type: {q_type}.',
        )

    if q_type in ('selectone', 'selectmany'):
        if 'values' not in q:
            raise InvalidQuestionError(
                'You must specify at least one choice for type choice.',
            )
        values = q['values']
        if values:
            if not isinstance(values, (list, tuple)):
                if not callable(values):
                    raise InvalidQuestionError(
                        'Choices must be a list, tuple of tuples or callable.',
                    )
            else:
                first_value = values[0]
                if not isinstance(first_value, (list, tuple)):
                    raise InvalidQuestionError(
                        'Choices must be a list or tuple of tuples.',
                    )
                if len(first_value) != 2:
                    raise InvalidQuestionError(
                        'Every choice must be a tuple (value, label).',
                    )

    if 'validators' in q:
        if not isinstance(q['validators'], (list, tuple)):
            raise InvalidQuestionError('Validators must be a list or tuple.')

        validator_instances = []
        for v in q['validators']:
            if not isinstance(v, (validators.Validator, dict)):
                raise InvalidQuestionError(
                    'Validators must be a list of  '
                    'interrogatio.validators.Validator'
                    ' instances or a list of validator objects.',
                )

            if isinstance(v, dict):
                _validate_validator_object(v)
                v = validators.get_instance(v)
                validator_instances.append(v)
            else:
                validator_instances.append(v)
        q['validators'] = validator_instances

    if 'disabled' in q:
        if not (isinstance(q['disabled'], bool) or callable(q['disabled'])):
            raise InvalidQuestionError(
                'Disabled flag must be a boolean or callable.',
            )


def validate_questions(questions):
    for q in questions:
        _validate_question(q)
