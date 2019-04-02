import argparse
import json
import sys
import os
import io

from . import interrogatio, dialogus


def _load_questions(args):
    questions = None
    with args.input as f:
        if args.input_format == 'json':
            questions = json.load(f)
        else:
            import yaml
            questions = yaml.load(f, Loader=yaml.FullLoader)
    return questions

def _write_answers(args, answers):
    with args.output as f:
        if args.input_format == 'json':
            json.dump(answers, f)
        else:
            import yaml
            yaml.dump(answers, f)


def main_dialogus():
    parser = argparse.ArgumentParser(description='dialogus')
    parser.add_argument('--input',
                        '-i',
                        type=argparse.FileType('r'),
                        required=True)
    parser.add_argument('--output',
                        '-o',
                        type=argparse.FileType('w'),
                        default=sys.stdout)

    parser.add_argument('--theme',
                        '-t',
                        default='default')

    parser.add_argument('--title')
    parser.add_argument('--confirm')
    parser.add_argument('--cancel')

    try:
        import yaml
        parser.add_argument('--input_format',
                            choices=['json', 'yml'],
                            default='json')
        parser.add_argument('--output_format',
                            choices=['json', 'yml'],
                            default='json')
    except ImportError:
        parser.set_defaults(input_format='json', output_format='json')

    args = parser.parse_args()

    kwargs = dict(
        theme=args.theme
    )
    if args.title:
        kwargs['title'] = args.title
    if args.confirm:
        kwargs['confirm'] = args.confirm
    if args.cancel:
        kwargs['cancel'] = args.cancel
    _write_answers(args, dialogus(_load_questions(args), **kwargs))

def main_interrogatio():
    parser = argparse.ArgumentParser(description='interrogatio')
    parser.add_argument('--input',
                        '-i',
                        type=argparse.FileType('r'),
                        required=True)
    parser.add_argument('--output',
                        '-o',
                        type=argparse.FileType('w'),
                        default=sys.stdout)

    parser.add_argument('--theme',
                        '-t',
                        default='default')


    try:
        import yaml
        parser.add_argument('--input_format',
                            choices=['json', 'yml'],
                            default='json')
        parser.add_argument('--output_format',
                            choices=['json', 'yml'],
                            default='json')
    except ImportError:
        parser.set_defaults(input_format='json', output_format='json')

    args = parser.parse_args()
    _write_answers(args, interrogatio(_load_questions(args),
                                      theme=args.theme))
