from .run import run

import argparse
import os


def main():
    parser = argparse.ArgumentParser(
        prog='codesters',
        description='Offline codesters library')
    parser.add_argument(
        'filename',
        help='[required]: the codesters python file to run',
        metavar='filename')
    parser.add_argument(
        '--example',
        '-e',
        help='Runs one of the example files from the codesters library (e.g. basketball.py)',
        action='store_true')

    args = parser.parse_args()

    filename = args.filename
    if args.example:
        filename = os.path.dirname(os.path.abspath(__file__)) + '/examples/' + filename

    run(filename)


if __name__ == '__main__':
    main()
