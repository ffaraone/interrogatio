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


def main():
    parser = argparse.ArgumentParser(description='Interrogatio')
    parser.add_argument('--input',
                        '-i',
                        type=argparse.FileType('r'),
                        required=True)
    parser.add_argument('--output',
                        '-o',
                        type=argparse.FileType('w'),
                        default=sys.stdout)
    subparsers = parser.add_subparsers()

    dialog_parser = subparsers.add_parser('dialog')
    dialog_parser.set_defaults(dialog=True)
    dialog_parser.add_argument('--title')
    dialog_parser.add_argument('--confirm')
    dialog_parser.add_argument('--cancel')

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
    if 'dialog' in args:
        kwargs = dict()
        if args.title:
            kwargs['title'] = args.title
        if args.confirm:
            kwargs['confirm'] = args.confirm
        if args.cancel:
            kwargs['cancel'] = args.cancel
        _write_answers(args, dialogus(_load_questions(args), **kwargs))
    else:
        _write_answers(args, interrogatio(_load_questions(args)))

    

if __name__ == '__main__':
    main()

