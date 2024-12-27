import os
import sys
import random

from .manager import Manager
from .environment import Environment

class App(object):

    def __init__(self, filename):
        self.manager = Manager()
        self.canvas = Manager.canvas
        self.root = Manager.root
        self.filename = filename
        self.canvas.pack()
        self.do()
        self.move_one()
        self.animate = None

    def do(self):
        global stage
        stage = Environment()
        filepath = self.filename
        try:
            exec(compile(open(filepath, "rb").read(), filepath, 'exec'), globals())
        except IOError:
            print("There is no file named "+filepath+". Please try again!")
        except SyntaxError:
            print(filepath+" is not a codesters Python file. Please try again!")

    def move_one(self):
        self.manager.run()
        self.animate = Manager.root.after(5, self.move_one)

def run(filename):
    app = App(filename)
    app.root.mainloop()
    sys.exit(0)

