import sys

print "Number of files: ", len(sys.argv)-1

# load JSON file
# search extension in JSON file
# return language
languages = {"c" : "C", "py": "Python"}

def cutFileName (fileName):
	return (fileName.rfind('.')+1, len(sys.argv[1])-1)

fileName = sys.argv[1]
initial, final = cutFileName (fileName)
extension = fileName [initial : final]
print languages [extension]
