#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Hakim Taklanti"
__copyright__ = "Copyright 2013, CEA / Saclay"
__credits__ = ["Hakim Taklanti", "Yann Cointepas", "Denis Rivière", "Nicolas Souedet"]
__license__ = "CeCILL v2"
__version__ = "0.1"
__maintainer__ = "Hakim Taklanti"
__email__ = "hakim.taklanti@altran.com"
__status__ = "dev"


import xml.etree.ElementTree as ET


class TagDependency(object):
	"Model dependency."

	@property
	def text(self):
		res = self.Name
		if self.Version:
			res = "%s - %s %s" % (self.Name,  self.Comparison, self.Version)
		return self.format(res)

	def __init__(self, name, version=None, comparison='', depends=True):
		self.Name = name
		self.Version = version
		self.Comparison = comparison
		self.Depends = depends

	def format(self, string):
		"Format to specify the version in QT"
		res = string.strip()
		res = res.replace(r'<<', r'<')
		res = res.replace(r'>>', r'>')
		res = res.replace(r';', r' ') 		
		return res