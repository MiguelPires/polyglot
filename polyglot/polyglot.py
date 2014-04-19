from __future__ import division
import os, yaml

class Polyglot:
	""" Polyglot searches for the file passed as an argument in the directories below the user's CWD.
	It does the same for the languages file."""

	def __init__(self, fileName, languagesFileArg = 'languages.yml'):
		self.baseFile = fileName
		self.languagesFile = self.tryOpenFile (languagesFileArg)
		self.languages = yaml.safe_load (self.languagesFile)
		self.totalFilesCounter = 0
		self.unknownLanguagesCounter = 0
		self.unknownLanguages = []
		self.ignoredLanguagesCounter = 0
		self.recognizedFilesCounter = 0
		self.languagesCounter = {"C": 0, "Python": 0}
		self.runAnalysis (fileName)

	def __repr__ (self):
		return self.knownLanguagesString() + self.unknownLanguagesString() + "\n" + self.ignoredLanguagesString()

	def __del__ (self):
		self.languagesFile.close()

	@staticmethod
	def tryOpenFile (file):
		try:
			return open(Polyglot.find (file) , 'r')
		except IOError, e:
		 	print e

	@classmethod
	def find (cls, name, root = os.getcwd()):
		for path, dirs, files in os.walk(root, False):
			if name in files or name in dirs:
				return os.path.join(path, name)
		
	def knownLanguagesString (self):
		if not self.totalFilesCounter == 0:
			v = str (round(self.recognizedFilesCounter / self.totalFilesCounter*100, 1))+ "% of the files were recognized. Recognized files:\n"
			for key, value in self.languagesCounter.iteritems():
				if not value == 0:
					v += "** " + str (key)+ ": " + str (round(value / self.totalFilesCounter*100, 1)) + "%\n"
			return v

		else:
			raise Exception ("No files were analyzed")

	def unknownLanguagesString (self):
		if not self.unknownLanguagesCounter == 0:
			return str (round(self.unknownLanguagesCounter / self.totalFilesCounter*100, 1))+ "% of the files were of unknown type. Unknown extensions:\n" + str (self.unknownLanguages)

	def ignoredLanguagesString(self):
		if not self.ignoredLanguagesCounter == 0:
			return str (round(self.ignoredLanguagesCounter / self.totalFilesCounter*100, 1))+ "% of the files were ignored. Ignored extensions:\n" + str (self.languages ['Ignore'])

	def getLanguageCounter (self, language):
		if language in languagesCounter:
			return self.languagesCounter [language] 

		else:
			raise KeyError ("Invalid language")

	@staticmethod
	def parseFileName (fileName):
		if fileName[0] == '\'' and fileName[len(fileName)-1] == '\'':
			fileName = fileName[1:len(fileName)-1] 

		return Polyglot.find (fileName)

	def generateExtensions (self):											# unused but pretty cool									
		for sublist in self.languages.values():
			for item in sublist:
				yield item

	def getListOfExtension (self, extension):								# returns the entire list of extensions where an extension belongs
		for sublist in self.languages.values():								# if the extension doesn't belong to any list, returns None
			if extension in sublist:
				return sublist
		
		return None

	def getLanguageFromExtensionList (self, list):							# returns the key associated with a value
		for key, value in self.languages.iteritems():						# the keys are language names and the values are lists of extensions
			if value == list:
				return key

		return None

	def updateStats (self, fileName):
		extension = fileName [fileName.rfind('.')+1 :]
		extList = self.getListOfExtension (extension)

		if extList == None:														# extension wasn't found in .yml
			self.unknownLanguagesCounter += 1

			if not extension in self.unknownLanguages:
				self.unknownLanguages.append (extension)

		else:
			languageName = self.getLanguageFromExtensionList (extList)		

			if languageName == "Ignore":									# ignored extensions
				self.ignoredLanguagesCounter += 1		

			else:
				self.languagesCounter [languageName] += 1
				self.recognizedFilesCounter += 1

		self.totalFilesCounter += 1

	def runAnalysis (self, fileName):
		filePath = self.parseFileName (fileName)

		if not os.path.exists (filePath):
			errMsg = "File \""+fileName+"\" doesn't exist."
			raise Exception (errMsg)

		if os.path.isfile (filePath):
			self.updateStats (fileName)

		elif os.path.isdir (filePath):
			contentList = os.listdir (filePath)
			for file in contentList:
				self.runAnalysis (file)

