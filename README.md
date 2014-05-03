Polyglot
========

Polyglot is a language detector written in Python 2.7.

It's heavily inspired in <a href="https://github.com/github/linguist"> Linguist </a>
by GitHub.

This project was born as a learning experience with the Python language. It's 
meant to be taken seriously but, still, is far from what Linguist is capable of.

We still have a lot to work on.

### Usage

There are two ways of running it: with or without the debug unknown languages' option. The debug option is a specific variable located at the top of the `polyglot.py` file which is `False` by default.

Running the program on its own `polyglot/` folder without the debug option:

    $ python polyglot.py ../polyglot/
    
    ** Python: 60.0%
    	polyglot\heuristics.py
    	polyglot\polyglot.py
    	polyglot\__init__.py

    ** YAML: 40.0%
    	polyglot\languages.yml
    	polyglot\syntax.yml
        

With the debug option:

    $ python polyglot.py ../polyglot/
    
    ** Python: 60.0%
    	polyglot\heuristics.py
    	polyglot\polyglot.py
    	polyglot\__init__.py

    ** YAML: 40.0%
    	polyglot\languages.yml
    	polyglot\syntax.yml
    Unknown extensions:
    'txt', 'pyc'

Apart from debug mode, there are still some options that impact the output of polyglot. If you run with `-h` option you can see all of it:

    $ python polyglot.py -h
    
    Polyglot supports the following searches:
        -p  programming languages only
        -d  data files only
        -a  every file
        -h  print help menu
    	
The `-a` flag is used by default if no option is used.

### Language Detection

#### Basic Detection

First we run a simple extension analyzer. Since most filename extensions aren't common to several languages, in most cases, specially with simple projects this works like a charm and is quite fast.

We run the `runAnalysis` recursively. This function interates differentiates between directories and files. If it's running with a file as an argument it calls `updateStats` to change the info, else, if it finds a directory, it runs itself with every file it finds as an argument.

#### Classifier

For trickier extensions like `.pl` (Prolog and Perl), `.h` (headers of most C variants), etc, we are building a classifier that runs heuristics to find the language in function of what's written on the file. For now it's pretty indecent but it'll work just fine.

### Installation

For the moment there's no installation *per se*. For now, just run the script
to get the output.

It the future there will probably exist one.

### Testing

We are still having some difficulties integrating the testing suite with the rest of the application. We're working hard on it.

### Contributing

For now, contributions will only be accepted for the `languages.yml` file because
the project is still under heavy development and, specially, lacking a definitive 
direction.

We want to understand where we want to go first, and go there, before we can have
other people on board.
