import argparse
import json
import sys
from functools import partial

try:
    import yaml
    FORMAT_CHOICES = ['json', 'yaml']
except ImportError:
    yaml = None
    FORMAT_CHOICES = ['json']


from interrogatio import dialogus, interrogatio


def _load_questions(args):
    with args.input as f:
        return args.deserialize(f)


def _write_answers(args, answers):
    with args.output as f:
        args.serialize(answers, f)


def _add_common_arguments(parser):
    parser.add_argument(
        '--input',
        '-i',
        type=argparse.FileType('r'),
        required=True,
        help='Input file with questions',
    )
    parser.add_argument(
        '--output',
        '-o',
        type=argparse.FileType('w'),
        default=sys.stdout,
        help='Output file to write answers to (Default: STDOUT)',
    )
    if len(FORMAT_CHOICES) > 1:
        parser.add_argument(
            '--input-format',
            choices=FORMAT_CHOICES,
            default='json',
            help='Questions file format (Default: json)',
        )
        parser.add_argument(
            '--output-format',
            choices=FORMAT_CHOICES,
            default='json',
            help='Answers file format (Default: json)',
        )
    parser.add_argument(
        '--theme',
        '-t',
        default='default',
        help='Name of the UI theme to use (Default: default)',
    )


def main_dialogus():
    parser = argparse.ArgumentParser(
        description='Show a wizard dialog to prompt user for questions.',
    )

    _add_common_arguments(parser)

    parser.add_argument(
        '--title',
        help='Title of the dialog',
    )
    parser.add_argument(
        '--intro',
        help='Specify the text of the introduction step (Default: no intro)',
    )
    parser.add_argument(
        '--summary',
        action='store_true',
        help=(
            'Show a summary with answers as the '
            'latest step (Default: no summary)'
        ),
    )

    for button in ('previous', 'next', 'cancel', 'finish'):
        cap_btn = button.capitalize()
        parser.add_argument(
            f'--{button}',
            default=cap_btn,
            help=(
                f'Customize the text of the "{button}" '
                f'button (Default: {cap_btn})'
            ),
        )

    args = parser.parse_args()

    if args.input_format == 'yaml':
        args.deserialize = partial(yaml.load, Loader=yaml.FullLoader)
        args.serialize = yaml.dump
    else:
        args.deserialize = json.load
        args.serialize = json.dump

    kwargs = {
        'intro': args.intro,
        'summary': args.summary,
        'title': args.title,
        'previous_text': args.previous,
        'next_text': args.next,
        'cancel_text': args.cancel,
        'finish_text': args.finish,
    }

    _write_answers(args, dialogus(_load_questions(args), **kwargs))


def main_interrogatio():
    parser = argparse.ArgumentParser(
        description='Prompt user for questions.',
    )
    _add_common_arguments(parser)

    args = parser.parse_args()

    if args.input_format == 'yaml':
        args.deserialize = partial(yaml.load, Loader=yaml.FullLoader)
        args.serialize = yaml.dump
    else:
        args.deserialize = json.load
        args.serialize = json.dump

    _write_answers(
        args,
        interrogatio(_load_questions(args), theme=args.theme),
    )
