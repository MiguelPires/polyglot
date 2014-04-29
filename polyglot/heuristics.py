
class Heuristics:


	""" Heuristics """
	def __init__(self, path, possibleLanguages):
		self.filePath = path
		self.possibleLanguages = possibleLanguages
		self.disambiguate(path, possibleLanguages)


	def disambiguate(self, path, languages):
		if "Perl" and "Prolog"  in languages:
			return self.disambiguate_pl (path);


	def disambiguate_pl (self, path):
		with open (path) as sourceCode:
			if ":-" in sourceCode.read():
				return "Prolog"

			sourceCode.seek (0)			#re-reads from the beginning of the file
			if  "#!/usr/local/bin/perl" in sourceCode.read():
				return "Perl"