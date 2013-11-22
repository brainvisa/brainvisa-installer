#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path

from brainvisa.installer.package import Package
from brainvisa.installer.component import Component
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage
from brainvisa.installer.bvi_utils.bvi_exception import BVIException

from brainvisa.compilation_info import packages_info
from brainvisa.maker.brainvisa_projects import brainvisaProjects, brainvisaComponentsPerProject


class Project(Component):
	"""BrainVISA project. A project is a set of packages.
	""" 

	@property
	def ifwname(self):
		"Return the BrainVISA Installer project name."
		p_name = self.name.replace('-', '_').lower()
		res = {
			'run' 		: "brainvisa.app.%s" % (p_name),
			'usrdoc'	: "brainvisa.app.%s" % (p_name),
			'dev'		: "brainvisa.dev.%s" % (p_name),
			'devdoc'	: "brainvisa.dev.%s" % (p_name)
		}
		return res[self.type]

	@property
	def ifwpackage(self):
		package = IFWPackage(
			DisplayName 	= self.name.title(), 
			Description 	= "%s project." % self.name.title(), 
			Version 		= self.version, 
			ReleaseDate 	= self.date, 
			Name 			= self.ifwname, 
			Virtual 		= 'false')
		return package

	def create(self, folder):
		for type_ in self.types:
			self.type = type_
			self.__create_subcategorie(folder)
			super(Project, self).create(folder)
		self.__create_pacakges(folder)

	def __init__(self, name, configuration, types = ['run', 'usrdoc', 'dev', 'devdoc']):
		if not name in brainvisaProjects:
			raise BVIException(BVIException.PROJECT_NONEXISTENT, name)
		super(Project, self)._Component__init_date()
		self.name = name
		self.project = name
		self.types = types
		self.type = None
		first_component = brainvisaComponentsPerProject[self.name][0]
		self.version = packages_info[first_component]['version']
		self.licenses = None
		self.data = None
		self.configuration = configuration

	def __create_subcategorie(self, folder):
		cat = self.configuration.category_by_id(self.type)
		name = "%s.%s" % (self.ifwname, self.type)
		folder_package = "%s/%s" % (folder, name)
		if os.path.isdir(folder_package):
			return
		os.mkdir(folder_package)
		os.mkdir("%s/meta" % folder_package)
		p = IFWPackage(	DisplayName = cat.Name, 
						Description = cat.Description, 
						Version 	= self.version, 
						ReleaseDate = self.date, 
						Name 		= name, 
						Virtual 	= 'false')
		p.save("%s/%s/meta/package.xml" % (folder, name))

	def __create_pacakges(self, folder):
		components = brainvisaComponentsPerProject[self.name]
		for package_name in components:
			for type_name in self.types:
				ext = '-%s' % type_name
				if type_name == 'run':
					ext = ''
				full_name = "%s%s" % (package_name, ext)
				if full_name in packages_info:
					Package(full_name).create(folder)