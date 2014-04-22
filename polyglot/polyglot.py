from __future__ import division
import os, yaml

class Polyglot:
	""" Polyglot searches for the file passed as an argument in or below the user's CWD.
	It does the same for the languages file. The file extensions are searched in a .yml file and statistics pertaining to
	the occurrences of known or unknown extensions are outputed"""

	def __init__ (self, fileName, languagesFileArg = 'languages.yml'):
		self.baseFile = fileName
		self.languagesFile = self.tryOpenFile (languagesFileArg)
		self.languages = yaml.safe_load (self.languagesFile)
		self.totalFilesCounter = 0
		self.recognizedFilesCounter = 0
		self.languagesCounter = {}
		self.unknownLanguagesCounter = 0
		self.unknownLanguages = []
		self.runAnalysis (fileName)

	def __repr__ (self):
		if not self.totalFilesCounter == 0:
			return self.knownLanguagesString() + self.unknownLanguagesString()				# the class representation - the analysis stats

		else:
			return "No files read."

	#def __del__ (self): 
		#self.languagesFile.close() #poop happening
	
	#*** String methods for printing output. Prints the percentages of each recognized file type, total recognized files, unknown extension, etc ***

	def knownLanguagesString (self):
		v = str (round(self.recognizedFilesCounter / self.totalFilesCounter*100, 1))+ "% of the files were recognized. Recognized files:\n"
		for key, counter in self.languagesCounter.iteritems():
				v += "** " + str (key)+ ": " + str (round(counter / self.totalFilesCounter*100, 1)) + "%\n"
		
		return v

	def unknownLanguagesString (self):
		if not self.unknownLanguagesCounter == 0:
			return str (round(self.unknownLanguagesCounter / self.totalFilesCounter*100, 1))+ "% of the files were of unknown type. Unknown extensions:\n" + str (self.unknownLanguages).strip('[]')

		else:
			return ""

	#*** Methods related to finding files below or in the current directory; used for finding and opening the YAML file ****

	@staticmethod
	def tryOpenFile (file):
		try:
			return open(Polyglot.find (file) , 'r')								# the corresponding .close() isn't coded yet 
		except IOError, e:
			print e

	@classmethod
	def find (cls, name, root = os.path.dirname (os.getcwd())):					# searches for the file in the current directory tree
		for path, dirs, files in os.walk(root, False):
			if name in files or name in dirs:
				return os.path.join(path, name)

		errorMsg = "File\\directory "+name+"was not found."						# 404: file not found
		raise Exception (errorMsg)


	@staticmethod
	def parseFileName (fileName):
		if fileName[0] == '\'' and fileName[len(fileName)-1] == '\'':
			fileName = fileName[1:len(fileName)-1]

		return Polyglot.find (fileName)


	def getListFromExtension (self, extension):                     # returns the of data of the language where 'extension' belongs
		for sublist in self.languages.values():                     # if extension isn't found, returns None
			if extension in sublist[0]:                             # sublist = [extensionsList]
				return sublist
		
		return None

	def getLanguageFromExtension (self, extension):
		dataList = self.getListFromExtension (extension)
		for key, value in self.languages.iteritems():             # returns the language name associated with an extension
			if value == dataList:
				return key

		return None

	def incrementLanguageCounter (self, language):
		if language in self.languagesCounter:			
			self.languagesCounter[language] += 1

		else:
			self.languagesCounter.update ({language: 1})

	def updateStats (self, fileName):										# checks the file extension and updates the respective counters 
		extension = fileName [fileName.rfind('.')+1 :]
		languageName = self.getLanguageFromExtension (extension)
	
		if languageName == None:                                            # extension wasn't found in .yml
			self.unknownLanguagesCounter += 1
			if extension not in self.unknownLanguages:
				self.unknownLanguages.append (extension)

		else:
				self.incrementLanguageCounter (languageName)				#extension was found (recognized) in .yml
				self.recognizedFilesCounter += 1

		self.totalFilesCounter += 1

	def runAnalysis (self, fileName):
		filePath = self.parseFileName (fileName)

		if not os.path.exists (filePath):									# no file or directory exists with 
			errMsg = "File \""+fileName+"\" doesn't exist."
			raise Exception (errMsg)

		if os.path.isfile (filePath):										# if the fileName is associated with a file, checks for its extension
			self.updateStats (fileName)

		elif os.path.isdir (filePath):										# if the fileName is associated with a directory, runs the check for each file within the directory (recursively)
			contentList = os.listdir (filePath)
			for file in contentList:
				self.runAnalysis (file)

