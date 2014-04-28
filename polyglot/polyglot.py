#!/usr/bin/env python
from __future__ import division
import os, sys, yaml

DEBUG_UNKNOWN = False

__author__ = "Miguel Pires, Hugo Martins"
__copyright__ = "Copyright 2014, Miguel Pires"
__license__ = "MIT"
__version__ = "0.1"
__status__ = "Prototype"

class Polyglot:
	""" Polyglot recieves either a path (relative or absolute) to a directory 
	or just a directory name. In case the argument is just a file name, Polyglot
	searches for the file passed in or below the user's CWD. It does the same 
	for the languages file. The file extensions are searched in a .yml file and 
	statistics pertaining to the occurrences of known or unknown extensions are 
	outputed to the terminal."""

	def __init__ (self, fileName, languagesFileArg = 'languages.yml'):
		self.initialPath = self.parseFileName (fileName)
		self.languagesFile = self.tryOpenFile (languagesFileArg)
		self.languages = yaml.safe_load (self.languagesFile)
		self.totalFilesCounter = 0
		self.languagesCounter = {}
		self.unknownLanguagesCounter = 0
		self.languagesFileNames = {}
		self.unknownLanguages = [] 
		self.runAnalysis (self.initialPath) 	# runs the analysis on the directory passes as an argument
		self.counterStats();

	def __repr__ (self):
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

	def knownLanguagesString (self):
		v = ""
		for key, counter in self.languagesCounter.iteritems():
				v += "** " + str (key) + ": " + str (counter * 100) + "%\n"
				filesList = self.languagesFileNames [key]
				for file in filesList:
					_, directory = os.path.split(self.initialPath)
					v += "\t" + directory + file [file.rfind(self.initialPath) + len(self.initialPath): ] + "\n"					
		
		return v

	def unknownLanguagesString (self):
		if not self.unknownLanguagesCounter == 0:
			return "Unknown extensions:\n" + str (self.unknownLanguages).strip('[]')

		else:
			return "No unknown languages"

	""" methods related to finding files below or in the current directory 
		used for finding and opening the YAML file.	"""

	@staticmethod
	def tryOpenFile (file):
		try:
			# the corresponding .close() isn't coded yet
			return open(Polyglot.find (file) , 'r')								 
		except IOError, e:
			print e

	# searches for the file in the current directory tree		
	@classmethod
	def find (cls, name, root = os.path.dirname (os.getcwd())):					
		for path, dirs, files in os.walk(root, False):
			if name in files or name in dirs:
				return os.path.join(path, name)

		errorMsg = "Directory "+name+" was not found." 	# 404: file not found
		raise Exception (errorMsg)


	@staticmethod
	def parseFileName (fileName):
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

	def getLanguageFromExtension (self, extension):
		dataList = self.getListFromExtension (extension)

		# returns the language name associated with an extension
		for key, value in self.languages.iteritems():             
			if value == dataList:
				return key

		return None

	def incrementLanguageCounter (self, language):
		if language in self.languagesCounter:			
			self.languagesCounter[language] += 1

		else:
			self.languagesCounter.update ({language: 1})

	# checks the file extension and updates the respective counters 
	def updateStats (self, fileName):										
		extension = fileName [fileName.rfind('.')+1 :]
		languageName = self.getLanguageFromExtension (extension)
		
		# extension wasn't found in .yml	
		if languageName == None:                                            
			self.unknownLanguagesCounter += 1
			if extension not in self.unknownLanguages:
				self.unknownLanguages.append (extension)

		else:	#extension was found (recognized) in .yml
			self.incrementLanguageCounter (languageName)				

			if languageName not in self.languagesFileNames:
				self.languagesFileNames.update ({languageName: [fileName]})

			else:
				self.languagesFileNames[languageName].append(fileName)

			self.totalFilesCounter += 1

	def runAnalysis (self, fileName):
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

if __name__ == '__main__':
	p = Polyglot (sys.argv[1])
	print p 
