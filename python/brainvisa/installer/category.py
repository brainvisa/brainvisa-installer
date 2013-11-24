#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from brainvisa.installer.component import Component
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage

# MODULE A SUPPRIMER

class Category(Component):
	"""Category for the BrainVISA installer. 

	Parameters
	----------
	name
	description
	version
	priority
	virtual
	"""

	@property
	def ifwname(self):
		pack_name = self.name.lower().replace('-', '_').replace(' ', '_')
		return "brainvisa.%s" % pack_name

	@property
	def ifwpackage(self):
		package = IFWPackage(
			DisplayName = self.name.title(), 
			Description = self.description, 
			Version = self.version, 
			ReleaseDate = self.date, 
			Name = self.ifwname, 
			Virtual = self.virtual,
			SortingPriority = self.priority)
		return package

	def __init__(self, name, description, version, priority, virtual):
		super(Category, self).__init_date()
		self.name = name
		self.description = description
		self.version = version
		self.priority = priority
		self.virtual = virtual
		self.type = None
		self.licenses = None
		self.data = None
		now = datetime.datetime.now()
		self.date = now.strftime("%Y-%m-%d")
