from prompt_toolkit.shortcuts import prompt

from .themes import get_default_theme


def _input(question, context):

    kwargs = dict(style=get_default_theme())


    output = [
        ('class:interrogatio.question', question['message']),
    ]

    if 'default' in question:
        kwargs['default'] = question['default']

    output.append(
        ('class:interrogatio.question', question.get('question_mark', ' ? '))
    )
    validators = question.get('validators', [])

    while True:
        answer = prompt(output, **kwargs)
        # validation_results = []
        # for validator in validators:
        #     try:
        #         validator(answer, context)
        #         validation_results.append(True)
        #     except ValidationError as ve:
        #         ve.show()
        #         validation_results.append(False)
        
        # if all(validation_results):
        #     return answer
    return answer