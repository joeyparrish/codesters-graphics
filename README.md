# codesters-graphics

A library to allow programs developed on codesters.com to run offline.

Now updated for Python 3!
See also [CHANGELOG.md](https://github.com/joeyparrish/codesters-graphics/blob/main/CHANGELOG.md).


## Synopsis

This is a python module to allow students working on www.codesters.com to run codesters projects offline.
The codesters-graphics library is also a great way to segue from structured lessons on codesters.com to
larger, object-oriented projects.


## Code Example

You can install the codesters library with pip.

```sh
python3 -m pip install codesters3
```

After installing the library with pip you can `import codesters` in any python file.
Either copy a project from www.codesters.com to a new python file or start making your own project in any new python file.
Most codesters projects will start with something like this:

```py
import codesters
stage = codesters.Environment()

sprite = codesters.Sprite("fox")
```

With the offline version you can also load your own sprite images. If you place a .gif image file in the same directory
as your python file you can load the image as a sprite. For example if you had a file called `narwhal.gif` you could make a sprite
like this:

```py
unicorn_of_the_sea = codesters.Sprite("narwhal")
```

You can also run a python file with the codesters graphics library like this:

```sh
codesters my_project_file.py
```

If you need inspiration, run one of our examples with

```sh
codesters --example basketball.py
```

Our example files are:
* basketball.py
* chainreaction.py
* feedthefish.py
* flappyfox.py
* flowerfox.py
* recycle.py


## Motivation

Codesters.com is a great way for a teacher to easily lead a class through lessons teaching Python programming via
interactive games and animations. The web based coding platform on codesters.com exposes a library of graphics,
animation, and game design tools that are not included with a basic Python installation. The codesters-graphics
project provides a similar graphical environment to allow a project created on codesters.com to be run in an
offline Python installation.

We at Codesters received requests from teachers who enjoyed working through lessons on codesters.com but wanted
to introduce students to working with a filesystem or working with other open source python modules within a
codesters project. The codesters-graphics library allows this transition.


## API Reference

Our documentation has just been started. There is a working sphinx-docs configuration in the docs directory with a
few documentation stubs in code to test the configuration.


## Contributing

The original version of this project appears to have been abandoned in 2015.  It was revived by
[joeyparrish](https://joeyparrish.github.io/) for his son at the beginning of 2025.  Issues and PRs on this fork
are very welcome.


## License

The codesters-graphics library is licensed under the MIT License.


## Packaging the module

```sh
python3 -m build
```
