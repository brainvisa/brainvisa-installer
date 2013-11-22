#!/usr/bin/env python
# -*- coding: utf-8 -*-

from brainvisa.installer.component import Component
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage
from brainvisa.installer.bvi_xml.tag_dependency import TagDependency
from brainvisa.compilation_info import packages_info, packages_dependencies


class Package(Component):

	@property
	def ifwname(self):
		"Return the BrainVISA Installer package name."
		p_name = self.project.replace('-', '_').lower()
		c_name = self.name.replace('-', '_').lower()
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
		deps = self.dependencies
		if self.licenses:
			if not deps:
				deps = list()
			for lic in self.licenses:
				license_component = "brainvisa.app.licenses.%s" % (lic.lower().replace('-', '_'))
				deps.append(TagDependency(name=license_component))

		package = IFWPackage(
			DisplayName = self.name.title(), 
			Description = '', 
			Version = self.version, 
			ReleaseDate = self.date, 
			Name = self.ifwname, 
			TagDependencies = deps, 
			Virtual = 'true',
			TagLicenses = None)
		return package

	def create(self, folder):
		super(Package, self).create(folder)
		if self.dependencies is None:
			return
		for dep in self.dependencies:
			if dep.Name in packages_info:
				Package(dep.Name).create(folder)
		
	def __init__(self, name):
		super(Package, self).__init__(name, True)
		self.dependencies = None
		self.__init_dependencies()

	def __init_dependencies(self):
		if not self.name in packages_dependencies:
			return
		infos_deps = list(packages_dependencies[self.name])
		res = list()
		for info in infos_deps:
			infos = packages_info[self.name]
			depends = True if info[0] == 'DEPENDS' else False
			d = TagDependency(
				name = info[1].decode('utf-8'), 
				version= info[2].decode('utf-8'), 
				depends=depends)
			res.append(d)
		self.dependencies =  res