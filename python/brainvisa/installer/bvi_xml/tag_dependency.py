#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TagDependency(object):
	"""Model dependency.

	Parameters
	----------
	name 		: name of dependency.
	version 	: Version number of the component in the following format: [0-9]+((.|-)[0-9]+)* such as 1-1; 1.2-2; 3.4.7.
	comparison  : =, >, <, >= or <=
	depends 	: False if the dependency is optional (this option is not taking into account in this current BrainVISA Installer.)
	"""

	@property
	def text(self):
		"""Format for the IFW package.xml file. The version numbers is \
		separated by a dash (-). 
		The version numbers is defined with a comparison operator (=, >, <, \
		>= or <=).
		"""
		separator = '' if self.Version == '' else '-'
		res = "%s%s%s%s" % (self.Name, separator, self.Comparison, self.Version)
		return self.escape(self.format(res))

	def __init__(self, name, version='', comparison='', depends=True):
		self.Name = name
		self.Version = version
		self.Comparison = comparison
		self.Depends = depends

	@classmethod
	def format(cls, string):
		"Format to specify the version in QT"
		res = string.strip()
		res = res.replace(r'<<', r'<')
		res = res.replace(r'>>', r'>')
		res = res.replace(r';', r' ') 		
		return res

	@classmethod
	def escape(cls, string):
		"Escape the invalid characters."
		res = string.strip()
		characters = {
			"\"" : "&quot;",
			"'" : "&apos;",
			"<" : "&lt;",
			">" : "&gt;",
			"&" : "&amp;",
			" " : ""}
		for char, escape in characters.iteritems():
			res = res.replace(char, escape)
		return res