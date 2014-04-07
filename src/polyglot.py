import sys
import os

languages = {"c" : "C", "py": "Python"}

def cutFileName (fileName):
	return fileName.rfind('.')+1

def polyglot (fileName):

	if fileName[0] == '\'' and fileName[len(fileName)-1] == '\'':
		fileName = fileName[1:len(fileName)-1] 

	filePath = os.path.abspath(fileName)

	if not os.path.exists (filePath):
		print "File doesn't exist"
		sys.exit()	

	if os.path.isfile (filePath):
		extensionIndex = cutFileName (fileName)
		extension = fileName [extensionIndex :]
		print languages [extension], "file"

	elif os.path.isdir (filePath):
		print "In directory:", fileName
		contentList = os.listdir (filePath)
		for file in contentList:
			polyglot (os.path.join(filePath, file))

polyglot (sys.argv[1])