from .environment import *
from .shapes import *
from .sprite import *
from .manager import *
from .run import run as codesters_run

import sys

# This can't be the best way to do this
# We want to skip this part when we use the command line tool (e.g. codesters --example flappyfox.py)
# We want to run this part when we just use python to run the file (e.g. python flappyfox.py)
# when we just use python, the first arg is the python file, thus:
if sys.argv[0].endswith('.py') and not sys.argv[0].endswith('pydoc.py'):
    codesters_run(sys.argv[0])

