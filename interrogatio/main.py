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

from . import interrogatio, dialogus


def _load_questions(args):
    with args.input as f:
        return args.deserialize(f)


def _write_answers(args, answers):
    with args.output as f:
        args.serialize(answers, f)


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

    parser.add_argument('--input-format',
                        choices=FORMAT_CHOICES,
                        default='json')
    parser.add_argument('--output-format',
                        choices=FORMAT_CHOICES,
                        default='json')

    args = parser.parse_args()

    if args.input_format == 'yaml':
        args.deserialize = partial(yaml.load, Loader=yaml.FullLoader)
        args.serialize = yaml.dump
    else:
        args.deserialize = json.load
        args.serialize = json.dump

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

    parser.add_argument('--input-format',
                        choices=FORMAT_CHOICES,
                        default='json')
    parser.add_argument('--output-format',
                        choices=FORMAT_CHOICES,
                        default='json')

    args = parser.parse_args()

    if args.input_format == 'yaml':
        args.deserialize = partial(yaml.load, Loader=yaml.FullLoader)
        args.serialize = yaml.dump
    else:
        args.deserialize = json.load
        args.serialize = json.dump

    _write_answers(args, interrogatio(_load_questions(args),
                                      theme=args.theme))
