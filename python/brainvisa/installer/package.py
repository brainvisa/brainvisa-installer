#!/usr/bin/env python
# -*- coding: utf-8 -*-


from brainvisa.installer.component import Component
import brainvisa.installer.bvi_utils.format as format
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage
from brainvisa.installer.bvi_xml.tag_dependency import TagDependency

from brainvisa.compilation_info import packages_dependencies


class Package(Component):
	"""BrainVISA package."""

	@property
	def ifwname(self):
		p_name = format.ifw_name(self.project)
		c_name = format.ifw_name(self.name)
		res = {
			'run' 		: "brainvisa.app.%s.run.%s" % (p_name, c_name),
			'usrdoc'	: "brainvisa.app.%s.usrdoc.%s" % (p_name, c_name),
			'dev'		: "brainvisa.dev.%s.dev.%s" % (p_name, c_name),
			'devdoc'	: "brainvisa.dev.%s.devdoc.%s" % (p_name, c_name),
			'thirdparty': "brainvisa.app.thirdparty.%s" % (c_name)
		}
		return res[self.type]

	@property
	def ifwpackage(self):
		tag_deps = list()
		if self.dependencies:
			for dep_pack in self.dependencies:
				tag_dep = TagDependency(
					name=dep_pack.ifwname, 
					version=dep_pack.version)
				tag_deps.append(tag_dep)
		if self.licenses:
			for lic in self.licenses:
				valid_name = format.ifw_name(lic)
				license_component = "brainvisa.app.licenses.%s" % valid_name
				tag_dep = TagDependency(name=license_component)
				tag_deps.append(tag_dep)

		package = IFWPackage(
			DisplayName = self.displayname, 
			Description = self.description, 
			Version = self.version, 
			ReleaseDate = self.date, 
			Name = self.ifwname, 
			TagDependencies = tag_deps, 
			Virtual = self.virtual,
			TagLicenses = None)
		return package

	def create(self, folder):
		super(Package, self).create(folder)
		if self.dependencies is None:
			return
		for dep_pack in self.dependencies:
			dep_pack.create(folder)
		
	def __init__(self, name, configuration=None):
		print "[ BVI ] -> PACKAGE: %s" % name
		super(Package, self).__init__(name, True, configuration)
		self.dependencies = None
		if self.displayname is None:
			self.displayname = self.name.title()
		self.__init_dependencies()

	def __init_dependencies(self):
		if not self.name in packages_dependencies:
			return
		infos_deps = list(packages_dependencies[self.name])
		if len(infos_deps) > 0:
			self.dependencies = list()
		for info in infos_deps:
			dep_name = info[1].decode('utf-8')
			dep_pack = Package(dep_name, self.configuration)
			self.dependencies.append(dep_pack)

	