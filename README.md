Polyglot
========

Polyglot is a language detector written in Python 2.7.

It's heavily inspired in <a href="https://github.com/github/linguist"> Linguist </a> by GitHub.

This project was born as a learning experience with the Python language. It's meant to be taken seriously but, still, is far from what Linguist is capable of.

We still have a lot to work on.

### Usage

Running the program on its on `polyglot/` folder:

    $ python daemon.py ../polyglot/
    
    83.3% of the files were recognized. Recognized files:
    ** Python: 67.0%
    ** YAML: 17.0%
    16.7% of the files were of unknown type. Unknown extensions:
    'pyc'
  
### Language Detection

### Installation

For the moment there's no installation *per se*. For now, just run the script to get the output.

It the future there will probably exist one.

### Contributing

For now, contributions will only be accepted for the `languages.yml` file because the project is still under heavy development and, specially, lacking a definitive direction.

We want to understand where we want to go first, and go there, before we can have other people on board.

### Todo

- Make sure the core functionalities are robust and well implemented.
- Create an analyser to classify languages that can be tricky.
- Understand what comes next.

