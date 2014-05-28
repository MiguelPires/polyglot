Polyglot
========

Polyglot is a language detector written in Python 2.7.

It's heavily inspired in <a href="https://github.com/github/linguist"> Linguist </a> by GitHub.

This project was born as a learning experience with the Python language. It's  meant to be taken seriously but, still, is far from what Linguist is capable of.

We still have a lot to work on.

	NAME:
        	polyglot - Know your languages. A language detector written in Python 2.7.
	USAGE:
        	python polyglot.py [options] [args]
	VERSION:
        	0.0.3
  	OPTIONS:
	        -p	print programming languages only
	        -d	print data files only
            -m  print markup files only
	        -a	print every file
	        --json	used before any of the above to produce JSON output
        
## Usage

Polyglot can be used a stand-alone application, it can be imported as a module or it can be used as a backend script producing JSON.
Furthermore, there is a debug unknown languages option and several flags to choose from.

### Arguments

When running Polyglot, as an app or by importing it as a module, there are some variants you can opt for. 
There are flags that narrow down the search to a specific type of file and also a debug option that includes unknown files in the output. You can read about them in the flags and debug chapters.

The only required argument is the file name that can be a relative or absolute path or just a file name (in which case Polyglot will try to find the file path). The optional flag argument must be one of the following strings `["all", "programming", "data", "markup"]`. `"all"` is the default value. Additionally, you can also use the `--json` option along with one of the flags to receive the output as valid JSON.
The debug argument can either be True or False, being False the default value.

#### Flags

Apart from this, there are still some flags that impact the output of polyglot. If you run with `-h` option you can see all of them:

    $ python polyglot.py -h
    
    Polyglot supports the following searches:
        -p  	programming languages only
        -d  	data files only
        -m      markup files only
        -a  	every file
        --json 	used before any of the above to produce JSON output
        -h  	print help menu
    	
The `-a` flag is used by default if no option is used. The `--json` flag is by default set to `False`. 

#### Debug

The debug option is a specific variable located at the top of the `polyglot.py` file which is `False` by default.
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

### Stand-alone app

There are two ways of running it as an app: with or without the debug unknown languages' option. The debug option is a specific variable located at the top of the `polyglot.py` file which is `False` by default.

Running the program on its own `polyglot/` folder in it's simplest form (without any flags or the debug option):

    $ python polyglot.py ../polyglot/
    
    ** Python: 60.0%
    	polyglot\heuristics.py
    	polyglot\polyglot.py
    	polyglot\__init__.py

    ** YAML: 40.0%
    	polyglot\languages.yml
    	polyglot\syntax.yml

### Module

If you want to integrate Polyglot in a different application, there is the possibility of importing it as a module. 
An simple example of this usage would be the following script:

	import polyglot

	fileName, flag = parseCommandLine()
	    
	if flag == -1:
		exit()

	poly = polyglot.Polyglot (fileName, flag)
	results = poly.startPolyglot()

	print results

Now an example that enables the debug option:

	import polyglot

	fileName, flag = polyglot.parseCommandLine()
	    
	if flag == -1:
		exit()

	poly = polyglot.Polyglot (fileName, flag, True)
	results = poly.startPolyglot()

	print "Files recognized:\n ", results[0]
	print "Files not recognized: \n", results[1]

As you can see, if the debug option is enabled Polyglot will return a tuple containing the language statistics dictionary in it's first index and an array containing every unkown extension found (stuff like build and compiled files will be the vast majority of what you see here).

### JSON output

If you want to get JSON output instead of those nasty strings, being it for use in a backend script with PHP or because you want to integrate the module with another language, this would be the result:

    $ python polyglot.py --json ../polyglot/
    
	{
	    "Python": 0.6,
	    "YAML": 0.4,
	    "nFiles": 5
	}

## Dependencies

- <a href="http://http://pyyaml.org/">PyYAML</a>

## Language Detection

Language detection works in three stages. If any of the stages succeds in identifying the file language, the next stages are not executed.

First, there is the basic detection stage, in which Polyglot tries to match the file extension with a language stored in a .yml file. If a file with a ambiguous extension (like .pl) is found, this stage fails and Polyglot moves on to the next stage of detection.

After that, there is the heuristics stage, in which Polyglot tries to disambiguate between multiple languages that can be assigned to a file.

Lastly, there is the (as of yet non-existent) classifier stage. This feature isn't implemented yet as we would like to solidify the basis of Polyglot before we move on.

### Basic Detection

First we run a simple extension analyzer. Since most filename extensions aren't common to several languages, in most cases, specially with simple projects this works like a charm and is quite fast.

We run the `runAnalysis` recursively. This function differentiates between directories and files. If it's running with a file as an argument it calls `updateStats` to update the info or, if it finds a directory, it runs itself with every file it finds as an argument.

### Heuristics

For extensions that Polyglot can't assign to a single language like '.pl' (Prolog and Perl) or '.h' (headers of most C variants), heuristics are employed to find the language in function of what's written on the file. Some language specific syntax strings (like ':-' for Prolog) are used as a way to disambiguate between languages. For now it's pretty indecent but it'll work just fine.

### Classifier

For extensions that cannot be disambiguated by the application of heuristics we are building a statistical classifier that determines what is the most likely language for the file in question.
