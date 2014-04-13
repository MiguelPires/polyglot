from __future__ import division
import sys, os

LANGUAGES = {"c" : "C", "py": "Python"}#, "pyc": "Python"}
languagesCounter = {"C": 0, "Python": 0}
totalFilesCounter = 0
unknownLanguagesCounter = 0
unknownLanguages = []

def cutFileName (fileName):
	extensionIndex = fileName.rfind('.')+1
	return fileName [extensionIndex :]

def checkFile (fileName):
	global languagesCounter, unknownLanguagesCounter, totalFilesCounter, LANGUAGES
	extension = cutFileName (fileName)

	if extension in LANGUAGES:
		languagesCounter [LANGUAGES [extension]] += 1
	else:
		unknownLanguagesCounter += 1

		if not extension in unknownLanguages:
			unknownLanguages.append(extension)

	totalFilesCounter += 1


def polyglot (fileName):

	if fileName[0] == '\'' and fileName[len(fileName)-1] == '\'':
		fileName = fileName[1:len(fileName)-1] 

	filePath = os.path.abspath(fileName)

	if not os.path.exists (filePath):
		print "File doesn't exist."
		sys.exit()	

	if os.path.isfile (filePath):
		checkFile (fileName)

	elif os.path.isdir (filePath):
		contentList = os.listdir (filePath)
		for file in contentList:
			polyglot (os.path.join(filePath, file))

if __name__ == '__main__':
	polyglot (sys.argv[1])

	for key, value in languagesCounter.iteritems():
		if not value == 0 or not totalFilesCounter == 0:
			print key+":", round(value/totalFilesCounter*100, 1), "%"

	if not unknownLanguagesCounter == 0:
		print round(unknownLanguagesCounter/totalFilesCounter*100, 1), "% of the files were of unknown type.\nUnknown extensions:", unknownLanguages





