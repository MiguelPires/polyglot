from __future__ import division
import os


class Polyglot:
	""" 1: At this point filePath is just the fileName and the CWD combined. Needs fixing.
	Maybe a walk through the OS directory tree will be needed to locate the directory.
		2: Add YAML parsing"""

	LANGUAGES = {"c" : "C", "py": "Python"}#, "pyc": "Python"}

	def __init__(self, fileName):
		self.baseFile = fileName
		self.totalFilesCounter = 0
		self.unknownLanguagesCounter = 0
		self.unknownLanguages = []
		self.languagesCounter = {"C": 0, "Python": 0}
		self.runAnalysis (fileName)

	def __repr__ (self):
		return self.knownLanguagesString() + self.unknownLanguagesString()

	def knownLanguagesString (self):
		if not self.totalFilesCounter == 0:
			v = ""
			for key, value in self.languagesCounter.iteritems():
				if not value == 0:
					v += str (key)+ ": " + str (round(value / self.totalFilesCounter*100, 1)) + "%\n"

			return v

		else:
			raise Exception ("No files were analyzed")

	def unknownLanguagesString (self):
		if not self.unknownLanguagesCounter == 0:
			return str (round(self.unknownLanguagesCounter / self.totalFilesCounter*100, 1))+ "% of the files were of unknown type.\nUnknown extensions:" + str (self.unknownLanguages)	+"\n"

	def getTotalFilesCounter (self):
		return self.totalFilesCounter

	def getUnknownLanguagesCounter (self):
		return self.unknownLanguagesCounter

	def getUnkownLanguages (self):
		return self.unknownLanguages

	def getLanguageCounter (self, language):
		if language in languagesCounter:
			return self.languagesCounter [language] 

		else:
			raise KeyError ("Invalid language")

	@staticmethod
	def parseFileName (fileName):
		if fileName[0] == '\'' and fileName[len(fileName)-1] == '\'':
			fileName = fileName[1:len(fileName)-1] 

		return os.path.abspath(fileName)

	def checkFile (self, fileName):
		extension = fileName [fileName.rfind('.')+1 :]

		if extension in self.LANGUAGES:
			self.languagesCounter [self.LANGUAGES [extension]] += 1
		else:
			self.unknownLanguagesCounter += 1

			if not extension in self.unknownLanguages:
				self.unknownLanguages.append (extension)

		self.totalFilesCounter += 1

	def runAnalysis (self, fileName):
		filePath = self.parseFileName (fileName)

		if not os.path.exists (filePath):
			raise Exception ("File \""+fileName+"\" doesn't exist.")

		if os.path.isfile (filePath):
			self.checkFile (fileName)

		elif os.path.isdir (filePath):
			contentList = os.listdir (filePath)
			for file in contentList:
				self.runAnalysis (os.path.join(filePath, file))

