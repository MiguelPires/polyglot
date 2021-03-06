#!/usr/bin/env python
from __future__ import division
import os
import sys
import getopt
import yaml
import json
import heuristics

DEBUG_UNKNOWN = False

__author__ = "Miguel Pires, Hugo Martins"
__copyright__ = "Copyright 2014, Miguel Pires"
__license__ = "MIT"
__version__ = "0.0.3"
__status__ = "Prototype"

class Polyglot (object):
    """ Polyglot recieves either a path (relative or absolute) to a directory 
    or just a directory name. In case the argument is just a file name, Polyglot
    searches for the file passed in or below the user's CWD. It does the same 
    for the languages file. The file extensions are searched in a .yml file and 
    statistics pertaining to the occurrences of known or unknown extensions are 
    outputed to the terminal."""

    def __init__ (self, fileName, flag="all", json=False, debug=False):

        # the path to the first directory passed to Polyglot
        self.initialPath = self.parseFileName (fileName)

        # output mode based on command line flags
        # possible flags: -p (programming files only), -d (data files only), -a (all [enabled by default])
        # flag checking in case Polyglot is wrongly used after being imported as a module
        if flag in ["all", "programming", "data", "markup"]:
            self.mode = flag

        else:
            raise ValueError ("Invalid flag passed as argument\n")

        #
        self.languagesFile = self.tryOpenFile ('languages.yml')

        # {language1: [extensions], language2: [extensions]}
        self.languages = yaml.safe_load (self.languagesFile)

        # the number of files analysed
        self.totalFilesCounter = 0

        # the total size of the files analysed
        self.totalBytesCounter = 0

        # contains a counter of occurrences for each language after runAnalysis is run
        # and a percentage (occurrences / totalFilesCounter) after counterStats is run
        self.languagesCounter = {}

        # contains the paths to the identified files of each language
        # {language1: [path_to_file, path_to_other_file], language2: []}
        self.languagesFileNames = {}

        # initially set at false, if this variable is changed to true, polyglot will
        # output the result in a json file
        self.json = jsonFlag

        # for debbugging purposes only - the DEBUG_UNKNOWN must be True
        # keeps the extensions and a counter for unknown extensions
        global DEBUG_UNKNOWN
        DEBUG_UNKNOWN = debug
        self.unknownLanguages = [] 
        self.unknownLanguagesCounter = 0
        

    def __repr__(self):
        if not self.totalFilesCounter == 0:

            # the class representation - the analysis stats
            representation = self.knownLanguagesString()
            if DEBUG_UNKNOWN:
            	representation += self.unknownLanguagesString()

            return representation

        else:
            return "No files read."

    """ string methods for printing output. Prints the percentages of each 
        recognized file type, total recognized files, unknown extension, etc.
    """

    def knownLanguagesString(self):
        out = ""
        for key, counter in self.languagesCounter.iteritems():
                out += "\n** " + str (key) + ": " + str (counter * 100) + "%\n"
                filesList = self.languagesFileNames[key]
                for file in filesList:
                    _, directory = os.path.split(self.initialPath)
                    out += "\t" + directory + file[file.rfind(self.initialPath) + len(self.initialPath): ] + "\n"                 
        
        return out

    def unknownLanguagesString(self):
        if not self.unknownLanguagesCounter == 0:
            return "Unknown extensions:\n" + str (self.unknownLanguages).strip('[]')

        else:
            return "No unknown languages"

    """ methods related to finding files below or in the current directory 
        used for finding and opening the YAML file. """



    @staticmethod
    def tryOpenFile(file):
        try:
            # the corresponding .close() isn't coded yet
            return open(Polyglot.find (file), 'r')                               
        except IOError, e:
            print e

    # searches for the file in the current directory tree       
    @classmethod
    def find(cls, name, root=os.path.dirname (os.getcwd())):                    
        for path, dirs, files in os.walk(root, False):
            if name in files or name in dirs:
                return os.path.join(path, name)

        errorMsg = "Directory "+name+" was not found."  # 404: file not found
        raise Exception (errorMsg)


    @staticmethod
    def parseFileName(fileName):
        if fileName[0] == '\'' and fileName[len(fileName)-1] == '\'':
            fileName = fileName[1:len(fileName)-1]

        # gets the absolute path if the argument was a relative path
        if '.' in fileName:                                                     
            filePath = os.path.abspath (fileName)

        # if the argument was an absolute path, uses it
        elif os.path.isabs(fileName):                                           
            filePath = fileName

        # if the argument was a directory name, finds the path to the directory
        else:                                                                   
            filePath = Polyglot.find (fileName)

        # no such file or directory exists
        if not os.path.exists (filePath):                                        
            errMsg = "File \""+fileName+"\" doesn't exist."
            raise Exception (errMsg)

        return filePath
  
    """ returns the of data of the language where 'extension' belongs
        if extension isn't found, returns None
        sublist = [extensionsList]
    """
    def getListFromExtension (self, extension):                     
        for sublist in self.languages.values():                     
            if extension in sublist[0]:                             
                return sublist
        
        return None

    def getLanguagesFromExtension(self, extension):
        # returns the language name associated with an extension
        languages = []

        for key, value in self.languages.iteritems():

            # only analyses the files relevant to the specified flag 
            if (self.mode == "all" or self.mode == value[1]) and extension in value[0]:
                languages.append (key)

        return languages

    # checks the file extension and updates the respective counters 
    def updateStats(self, fileName):                                        
        extension = fileName [fileName.rfind('.')+1 :]
        languageNames = self.getLanguagesFromExtension (extension)

  		# extension wasn't found in .yml       
        if len (languageNames) == 0:                                      
            self.unknownLanguagesCounter += 1
            if extension not in self.unknownLanguages:
                self.unknownLanguages.append (extension)

		#extension's language was found (recognized) in .yml
        elif len (languageNames) == 1:   
            self.languageOccurrence (fileName, languageNames[0])

		#disambiguate between multiple languages
        elif len (languageNames) > 1:       
            h = heuristics.Heuristics (fileName, languageNames)
            finalLanguage = h.disambiguate (fileName, languageNames)

			#language was decided
            if finalLanguage != None:       
                self.languageOccurrence (fileName, finalLanguage)

    # updates everything related to the occurrence of a known extension
    def languageOccurrence(self, fileName, language):

        # gets the file size
        size = os.stat(fileName)[6]

        # ignores empty files
    	if size != 0:
            size = os.stat(fileName)[6]
            self.incrementLanguageCounter (language, size)                

            if language not in self.languagesFileNames:
                self.languagesFileNames.update ({language: [fileName]})

            else:
                self.languagesFileNames[language].append(fileName)

            self.totalBytesCounter += size
            self.totalFilesCounter += 1

    #updates the occurrences of a language based on the file size
    def incrementLanguageCounter(self, language, size):
        if language in self.languagesCounter:          
            self.languagesCounter[language] += size

        else:
            self.languagesCounter.update ({language: size})

    # runs the analysis on the directory passed as an argument
    def startPolyglot(self):
        self.runAnalysis(self.initialPath)    
        self.counterStats()

        if DEBUG_UNKNOWN:
            return self.languagesCounter, self.unknownLanguages
        else:
            return self.languagesCounter

    def runAnalysis(self, fileName):
        filePath = self.parseFileName (fileName)

        # if the fileName is associated with a file, checks for its extension
        if os.path.isfile (filePath):                                       
            self.updateStats (fileName)

        # if is directory, runs the check for each file within the directory 
        elif os.path.isdir (filePath):  

        # ignores vendor files
            if "vendor" not in fileName:                             
                contentList = os.listdir (filePath)
                for file in contentList:
                    self.runAnalysis (os.path.join (filePath, file))

    def counterStats(self):
        for key, value in self.languagesCounter.iteritems():
            self.languagesCounter[key] = round(value / self.totalBytesCounter, 3)

def parseCommandLine ():
    
    jsonFlag = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hpdma", ["json"])

    except getopt.GetoptError:
        print helpText()
        return None, -1
    
    # only supports one flag
    for flag in opts:
        if '-p' in flag:
            return args[0], "programming", jsonFlag   # programming files only
        
        elif '-d' in flag:                  # data files only
            return args[0], "data", jsonFlag

        elif '-m' in flag:
            return args[0], "markup", jsonFlag

        elif '-a' in flag:                  # all files
            return args[0], "all", jsonFlag

        elif '--json' in flag:				# output will be json
        	jsonFlag = True

        else:                               # help
            print helpText()
            return None, -1, jsonFlag

    return args[0], "all", jsonFlag

def JSON(self):

	self.languagesCounter["nFiles"] = self.totalFilesCounter
	print json.dumps(self.languagesCounter, sort_keys=True, indent=4, separators=(',', ': '))
	

def helpText():
  return "\n    NAME:\n\
        polyglot - Know your languages. A language detector written in Python 2.7.\
            \n\n    USAGE:\n\
        python polyglot.py [options] [args]\
            \n\n    VERSION:\n\
        0.0.3\
            \n\n    OPTIONS:\n\
        -p\tprint programming languages only\n\
        -d\tprint data files only\n\
        -a\tprint every file\n\
        --json\tused before any of the above to produce JSON output"

if __name__ == '__main__':

    fileName, flag, jsonFlag = parseCommandLine()
    if flag == -1:
        exit()

    polyglot = Polyglot (fileName, flag, jsonFlag)
    polyglot.startPolyglot()

    if jsonFlag:
    	JSON(polyglot)
    else:
    	print polyglot 

