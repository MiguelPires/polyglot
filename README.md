Polyglot
========

Polyglot is a language detector written in Python 2.7.

It's heavily inspired in <a href="https://github.com/github/linguist"> Linguist </a>
by GitHub.

This project was born as a learning experience with the Python language. It's 
meant to be taken seriously but, still, is far from what Linguist is capable of.

We still have a lot to work on.

### Usage

Running the program on its own `polyglot/` folder without the debug option:

    $ python polyglot.py ../polyglot/
    
    ** Python: 75.0%
    	polyglot\polyglot\polyglot.py
    	polyglot\polyglot\test.py
    	polyglot\polyglot\__init__.py

    ** YAML: 25.0%
    	polyglot\polyglot\languages.yml
        

With the debug option:

    $ python polyglot.py ../polyglot/
    
    ** Python: 75.0%
    	polyglot\polyglot\polyglot.py
    	polyglot\polyglot\test.py
    	polyglot\polyglot\__init__.py

    ** YAML: 25.0%
    	polyglot\polyglot\languages.yml
    Unknown extensions:
    'txt', 'pyc'


  
### Language Detection

For now we have a simple filename extension analyzer that runs recursively through
the directory and checks the extensions against the `languages.yml` file.

### Installation

For the moment there's no installation *per se*. For now, just run the script
to get the output.

It the future there will probably exist one.

### Contributing

For now, contributions will only be accepted for the `languages.yml` file because
the project is still under heavy development and, specially, lacking a definitive 
direction.

We want to understand where we want to go first, and go there, before we can have
other people on board.

### Todo

- Make sure the core functionalities are robust and well implemented.
- Create an analyser to classify languages that can be tricky.
- Understand what comes next.
