import os, sys, random, string, polyglot
directoryList = []

def createDirectory ():
	fullPath = os.path.abspath (sys.argv[0])
	directory, _ = os.path.split (fullPath)
	
	randomChar = random.choice (string.letters)
	newDir = os.path.join(directory, randomChar)

	while os.path.exists (newDir):
		randomChar = random.choice (string.letters)
		newDir = os.path.join(directory, randomChar)

	directoryList.append (newDir)
	os.mkdir (newDir)


def eraseDirectories ():
	for dir in directoryList:
		os.unlink (dir)
		