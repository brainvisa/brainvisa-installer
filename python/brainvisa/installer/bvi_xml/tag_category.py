#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ 		= "Hakim Taklanti"
__copyright__ 	= "Copyright 2013, CEA / Saclay"
__credits__ 	= ["Hakim Taklanti", "Yann Cointepas", "Denis Rivière", "Nicolas Souedet"]
__license__ 	= "CeCILL v2"
__version__ 	= "0.1"
__maintainer__ 	= "Hakim Taklanti"
__email__ 		= "hakim.taklanti@altran.com"
__status__ 		= "dev"


import xml.etree.ElementTree as ET


class TagCategory(object):
	"Tag Category in BrainVISA Installer XML configuration file."

	def __init__(self, id_ = None, name = None, description = None, version = None, priority = None, default = None, subcategories = None):
		self.Id = id_
		self.Name = name
		self.Description = description
		self.Version = version
		self.Priority = priority
		self.Default = default
		self.Subcategories = subcategories

	def init_from_configuration(self, element, childs=None):
		"Initialize from an XML element from XML configuration file."
		self.Id = element.attrib.get('ID')
		self.Name = element.attrib.get('NAME')
		self.Description = element.attrib.get('DESCRIPTION')
		self.Version = element.attrib.get('VERSION')
		self.Priority = element.attrib.get('PRIORITY')
		self.Default = element.attrib.get('DEFAULT', 'false')
		self.Subcategories = childs
		return self