#!/usr/bin/env python
from __future__ import division
import os
import sys
import getopt
import yaml
import heuristics

DEBUG_UNKNOWN = False

__author__ = "Miguel Pires, Hugo Martins"
__copyright__ = "Copyright 2014, Miguel Pires"
__license__ = "MIT"
__version__ = "0.1"
__status__ = "Prototype"

class Polyglot (object):
    """ Polyglot recieves either a path (relative or absolute) to a directory 
    or just a directory name. In case the argument is just a file name, Polyglot
    searches for the file passed in or below the user's CWD. It does the same 
    for the languages file. The file extensions are searched in a .yml file and 
    statistics pertaining to the occurrences of known or unknown extensions are 
    outputed to the terminal."""

    def __init__ (self, fileName, flag = "all", languagesFileArg='languages.yml'):

        # the path to the first directory passed to Polyglot
        self.initialPath = self.parseFileName (fileName)

        # output mode based on command line flags
        # possible flags: -p (programming files only), -d (data files only), -a (all [enabled by default])
        self.mode = flag

        #
        self.languagesFile = self.tryOpenFile (languagesFileArg)

        # {language1: [extensions], language2: [extensions]}
        self.languages = yaml.safe_load (self.languagesFile)

        self.totalFilesCounter = 0

        # contains a counter of occurrences for each language after runAnalysis is run
        # and a percentage (occurrences / totalFilesCounter) after counterStats is run
        self.languagesCounter = {}

        # contains the paths to the identified files of each language
        # {language1: [path_to_file, path_to_other_file], language2: []}
        self.languagesFileNames = {}

        # for debbugging purposes only - the DEBUG_UNKNOWN must be True
        # keeps the extensions and a counter for unknown extensions
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

            # only analyses the files relevant to the flag specified
            if (self.mode == "all" or self.mode == value[1]) and extension in value[0]:
                languages.append (key)

        return languages

    # checks the file extension and updates the respective counters 
    def updateStats(self, fileName):                                        
        extension = fileName [fileName.rfind('.')+1 :]
        languageNames = self.getLanguagesFromExtension (extension)

        if len (languageNames) == 0:            # extension wasn't found in .yml                                   
            self.unknownLanguagesCounter += 1
            if extension not in self.unknownLanguages:
                self.unknownLanguages.append (extension)

        elif len (languageNames) == 1:   #extension's language was found (recognized) in .yml
            self.languageOccurrence (fileName, languageNames[0])

        elif len (languageNames) > 1:       #disambiguate between multiple languages
            h = heuristics.Heuristics (fileName, languageNames)
            finalLanguage = h.disambiguate (fileName, languageNames)

            if finalLanguage != None:       #language was decided
                self.languageOccurrence (fileName, finalLanguage)

            #else:              #language still wasn't decided

    # updates everything related to the occurrence of a known extension
    def languageOccurrence(self, fileName, language):
        self.incrementLanguageCounter (language)                

        if language not in self.languagesFileNames:
            self.languagesFileNames.update ({language: [fileName]})

        else:
            self.languagesFileNames[language].append(fileName)

        self.totalFilesCounter += 1

    def incrementLanguageCounter(self, language):
        if language in self.languagesCounter:           
            self.languagesCounter[language] += 1

        else:
            self.languagesCounter.update ({language: 1})

    def startPolyglot(self):
        # runs the analysis on the directory passed as an argument
        self.runAnalysis(self.initialPath)    
        self.counterStats()

    def runAnalysis(self, fileName):
        filePath = self.parseFileName (fileName)

        # if the fileName is associated with a file, checks for its extension
        if os.path.isfile (filePath):                                       
            self.updateStats (fileName)

        # if is directory, runs the check for each file within the directory 
        elif os.path.isdir (filePath):                                      
            contentList = os.listdir (filePath)
            for file in contentList:
                self.runAnalysis (os.path.join (filePath, file))

    def counterStats(self):
        for key, value in self.languagesCounter.iteritems():
            self.languagesCounter[key] = round(value / self.totalFilesCounter, 2)

def parseCommandLine ():
    opts, args = getopt.getopt(sys.argv[1:], "hpda")

    # only supports one flag
    for flag in opts:
        if '-p' in flag:
            return args[0], "programming"   # programming files only
        
        elif '-d' in flag:                  # data files only
            return args[0], "data"

        elif '-a' in flag:                  # all files
            return args[0], "all"

        else:                               # help
            print "\n    NAME:\n\
        polyglot - Know your languages. A language detector written in Python 2.7.\
            \n\n    USAGE:\n\
        python polyglot.py [options] [args]\
            \n\n    VERSION:\n\
        0.0.2\
            \n\n    OPTIONS:\n\
        -p    print programming languages only\n\
        -d    print data files only\n\
        -a    print every file"
            return None, -1

    return args[0], "all"
    
if __name__ == '__main__':

    fileName, flag = parseCommandLine()
    if flag == -1:
        exit()

    polyglot = Polyglot (fileName, flag)
    polyglot.startPolyglot()
    print polyglot 
