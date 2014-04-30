import polyglot
import yaml

class Heuristics (object):


	""" The Heuristics class receives a path to the file that is trying to be
	identified and an array of possible languages for that file. The disambiguate
	method will find the array with unambiguous strings of syntax for each language
	and check the file in question for those strings. If a match occurrs then the file is
	unquestionably written in the language that the string belongs to. If no match
	is found then None is returned and the file wasn't determined to be of a
	particular language."""


	def __init__(self, path, possibleLanguages):
		self.syntaxFile = polyglot.Polyglot.tryOpenFile ('syntax.yml')

		# {language1: [bits_of_syntax1, bits_of_syntax2], language2: [bits_of_syntax3, bits_of_syntax4]}
		self.syntaxBits = yaml.safe_load (self.syntaxFile)
		self.disambiguate(path, possibleLanguages)

	def disambiguate(self, path, possibleLanguages):
		#checks the syntax strings of every possible language until it finds a match

		with open (path) as sourceCode:
			for lang in possibleLanguages:
				if lang not in self.syntaxBits.keys():
					continue	#there are no stored syntax strings for that language

				else:
					for string in self.syntaxBits [lang]:
						if string in sourceCode.read():
							return lang
						
						sourceCode.seek (0)			#re-reads from the beginning of the file
		return None
