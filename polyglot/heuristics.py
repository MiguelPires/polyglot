import polyglot
import yaml

class Heuristics:


	""" Heuristics """


	def __init__(self, path, possibleLanguages):
		self.syntaxFile = polyglot.Polyglot.tryOpenFile ('syntax.yml')
		self.syntaxBits = yaml.safe_load (self.syntaxFile)
		self.disambiguate(path, possibleLanguages)

	def disambiguate(self, path, possibleLanguages):
		#checks the syntax strings of every possible language until it finds a match

		with open (path) as sourceCode:
			for lang in possibleLanguages:
				if lang not in self.syntaxBits.keys():
					continue		#there are syntax strings for that language

				else:
					for string in self.syntaxBits [lang]:
						if string in sourceCode.read():
							return lang
						
						sourceCode.seek (0)			#re-reads from the beginning of the file
