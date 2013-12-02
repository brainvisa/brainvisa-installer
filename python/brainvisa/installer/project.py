#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import collections

from brainvisa.installer.package import Package
from brainvisa.installer.component import Component
import brainvisa.installer.bvi_utils.format as format
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage
from brainvisa.installer.bvi_xml.tag_dependency import TagDependency
from brainvisa.installer.bvi_utils.bvi_exception import BVIException

from brainvisa.compilation_info import packages_info
from brainvisa.maker.brainvisa_projects import brainvisaProjects
from brainvisa.maker.brainvisa_projects import brainvisaComponentsPerProject


class Project(Component):
	"""BrainVISA project. 

	A project contains a set of packages.

	Parameters
	----------
	name 			: BrainVISA project name. It must be in brainvisa_projects module. 
	configuration	: Configuration object, using to configure the subcategory for each 
					  project (see CATEGORY section).
	types			: list of type's names: run, usrdoc, dev, devdoc. 
					  Default: ['run', 'usrdoc', 'dev', 'devdoc']
	""" 

	@property
	def ifwname(self):
		p_name = format.ifw_name(self.name)
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
		self.__create_pacakges(folder)
		for type_ in self.types:
			self.type = type_
			self.__create_subcategorie(folder)
			super(Project, self).create(folder)

	def __init__(self, name, configuration, types = None): #pylint: disable=W0231
		print "[ BVI ] => PROJECT: %s" % name
		types = types or ['run', 'usrdoc', 'dev', 'devdoc']
		if not name in brainvisaProjects:
			raise BVIException(BVIException.PROJECT_NONEXISTENT, name)
		super(Project, self)._Component__init_date()
		self.name = name
		self.project = name
		self.types = types
		self.type = None
		self.configuration = configuration
		self.licenses = None
		self.data = None
		self.dep_packages = collections.defaultdict(list)
		first_component = brainvisaComponentsPerProject[self.name][0]
		ex_version = self.configuration.exception_by_name(first_component,
			'VERSION')
		if ex_version is None:
			self.version = packages_info[first_component]['version']
		else:
			self.version = ex_version

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
						Virtual 	= 'false',
						TagDependencies = self.__clean_dependencies_doublons())
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
					pack = Package(full_name, self.configuration)
					pack.create(folder)
					if not self.__is_in_dependencies(pack, type_name):
						self.dep_packages[type_name].append(pack)

	def __is_in_dependencies(self, package, type_name):
		for dep in self.dep_packages[type_name]:
			if dep.ifwname == package.ifwname:
				return True
		return False

	@classmethod
	def __is_in_tagdependencies(cls, tagdepency, tagdependencies):
		for tag in tagdependencies:
			if tag.text == tagdepency:
				return True
		return False

	def __clean_dependencies_doublons(self):
		clean_tagdependencies = list()
		for dep_pack in self.dep_packages[self.type]:
			tagdependency = TagDependency(
				name=dep_pack.ifwname, 
				version=dep_pack.version, 
				comparison='=')
			if not self.__is_in_tagdependencies(tagdependency, clean_tagdependencies):
				clean_tagdependencies.append(tagdependency)					
		return clean_tagdependencies

