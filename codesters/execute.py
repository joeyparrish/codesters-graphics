from . import run
from . import example
import argparse


def execute(filename):
    run.run(filename)


def execute_example(filename):
    example.run(filename)


def runner():
    parser = argparse.ArgumentParser(
        usage="\nThis command runs codesters files. \
        A default command would be as follows:\n\n codesters <options> filename\n",
        description="Offline codesters library",
        epilog="",
        )
    parser.add_argument(
        "filename",
        help="REQUIRED ARGUMENT: the codesters python file in the current directory to run",
        metavar="filename")
    parser.add_argument(
        "-e",
        "--example",
        help="runs one of the example files from the codesters library (e.g. basketball.py)",
        action="store_true")

    args = parser.parse_args()

    filename = args.filename

    if args.example:
        filename = os.path.dirname(os.path.abspath(__file__)) + '/examples/' + filename

    execute(filename)
