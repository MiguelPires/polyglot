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
		self.recognizedFilesCounter = 0
		self.runAnalysis (fileName)

	def __repr__ (self):
		if not self.totalFilesCounter == 0:
			return self.knownLanguagesString() + self.unknownLanguagesString() + "\n" + self.ignoredLanguagesString()

		else:
			return "No files read."

	def __del__ (self): 
		"""with open ('output.yaml', 'w') as output:	
			output.write (yaml.dump (self.languages, output, default_flow_style=True))
		self.languagesFile.close()""" #poop happening

	@staticmethod
	def tryOpenFile (file):
		try:
			return open(Polyglot.find (file) , 'r+')
		except IOError, e:
		 	print e

	@classmethod
	def find (cls, name, root = os.getcwd()):
		for path, dirs, files in os.walk(root, False):
			if name in files or name in dirs:
				return os.path.join(path, name)

	def knownLanguagesString (self):
		v = str (round(self.recognizedFilesCounter / self.totalFilesCounter*100, 1))+ "% of the files were recognized. Recognized files:\n"
		for key, value in self.languages.iteritems():
			languagecounter = value[1]
			if not languagecounter == 0 and key != 'Ignore' and key != 'Unknown':
				v += "** " + str (key)+ ": " + str (round(languagecounter / self.totalFilesCounter*100, 1)) + "%\n"
		
		return v

	def unknownLanguagesString (self):
		unknownLanguagesCounter = self.languages ['Unknown'][1]
		if not unknownLanguagesCounter == 0:
			return str (round(unknownLanguagesCounter / self.totalFilesCounter*100, 1))+ "% of the files were of unknown type. Unknown extensions:\n" + str (self.languages ['Unknown'][0]).strip('[]')

		else:
			return ""

	def ignoredLanguagesString(self):
		ignoredLanguagesCounter = self.languages ['Ignore'][1]
		if not ignoredLanguagesCounter == 0:
			return str (round(ignoredLanguagesCounter / self.totalFilesCounter*100, 1))+ "% of the files were recognized but ignored. Ignored extensions:\n" + str (self.languages ['Ignore'][0]).strip('[]')
		else:
			return ""

	@staticmethod
	def parseFileName (fileName):
		if fileName[0] == '\'' and fileName[len(fileName)-1] == '\'':
			fileName = fileName[1:len(fileName)-1] 

		return Polyglot.find (fileName)

	def generateExtensions (self):											# unused but pretty cool									
		for sublist in self.languages.values():
			for item in sublist:
				yield item

	def generateSublist (self):											# unused but pretty cool									
		for sublist in self.languages.values():
			yield sublist

	def getListFromExtension (self, extension):						# returns the of data of the language where 'extension' belongs
		for sublist in self.languages.values():						# if extension isn't found, returns None
			if extension in sublist[0]:								# sublist = [extensionsList, counter]
				return sublist

		return None

	def getLanguageFromExtension (self, extension):						# returns the language name associated with an extension
		dataList = self.getListFromExtension (extension)
		for key, value in self.languages.iteritems():					
			if value == dataList:
				return key

		return None

	def incrementLanguageCounter (self, extension):
		self.incrementLanguageCounter (self.getLanguageFromExtension (extension))

	def incrementLanguageCounter (self, language):
		self.languages[language][1] += 1

	def updateStats (self, fileName):
		extension = fileName [fileName.rfind('.')+1 :]
		languageName = self.getLanguageFromExtension (extension)
	
		if languageName == None:														# extension wasn't found in .yml
			if extension not in self.languages['Unknown'][0]:
				self.languages['Unknown'][0].append (extension)

			self.languages['Unknown'][1] += 1
			# encontrar o UNKOWN, incrementar o contador e adicionar a extensao	

		else:
				self.incrementLanguageCounter (languageName)
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

