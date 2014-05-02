#!/usr/bin/env python
import unittest
from .. import polyglot

class TestOne(unittest.TestCase):

	def testTrue(self):
		self.assertTrue(1)

if __name__ == '__main__':
	unittest.main()