# Change log

Since forking away from https://github.com/learningcom/codesters-graphics, the following high-level changes have been made:


## 1.0.0

 - Update README
 - Replace `setup.py` packaging with modern `build`-based packaging and `pyproject.toml`
 - Convert Python 2 code to Python 3
 - Update dependency versions
 - Fix exceptions thrown after running user script
 - Add automated publication workflow in GitHub Actions


## 1.0.1

 - Fix bad dependency specification in 1.0.0 release


## 1.1.0

 - Fix TK window creation when importing module in REPL
 - Clean up script loading code and CLI
 - Fix broken examples
 - Fix compatibility with pydoc
 - Fix use-before-assignment bugs
 - Add all codesters sprites from codesters API, optimized and compressed


## Future

 - Automated docs generation
 - Documentation for available sprites
 - Auto-complete for available sprites in VS Code
