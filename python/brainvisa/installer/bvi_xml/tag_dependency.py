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
		res = self.Name
		if self.Version:
			res = "%s - %s %s" % (self.Name,  self.Comparison, self.Version)
		return self.format(res)

	def __init__(self, name, version=None, comparison='', depends=True):
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