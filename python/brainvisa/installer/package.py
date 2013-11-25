#!/usr/bin/env python
# -*- coding: utf-8 -*-

from brainvisa.installer.component import Component
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage
from brainvisa.installer.bvi_xml.tag_dependency import TagDependency
from brainvisa.compilation_info import packages_info, packages_dependencies


class Package(Component):
	"""BrainVISA package."""

	@property
	def ifwname(self):
		p_name = self.__valid_name(self.project)
		c_name = self.__valid_name(self.name)
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
				tag_dep = TagDependency(name=dep_pack.ifwname, 
					version=dep_pack.version)
				tag_deps.append(tag_dep)
		if self.licenses:
			for lic in self.licenses:
				valid_name = self.__valid_name(lic)
				license_component = "brainvisa.app.licenses.%s" % valid_name
				tag_dep = TagDependency(name=license_component)
				tag_deps.append(tag_dep)

		package = IFWPackage(
			DisplayName = self.name.title(), 
			Description = '', 
			Version = self.version, 
			ReleaseDate = self.date, 
			Name = self.ifwname, 
			TagDependencies = tag_deps, 
			Virtual = 'true',
			TagLicenses = None)
		return package

	def create(self, folder):
		super(Package, self).create(folder)
		if self.dependencies is None:
			return
		for dep_pack in self.dependencies:
			if dep_pack.name in packages_info:
				dep_pack.create(folder)
			# if dep.Name in packages_info:
			# 	Package(dep.Name).create(folder)
		
	def __init__(self, name):
		super(Package, self).__init__(name, True)
		self.dependencies = None
		self.__init_dependencies()

	def __init_dependencies(self):
		if not self.name in packages_dependencies:
			return
		infos_deps = list(packages_dependencies[self.name])
		# res = list()
		if len(infos_deps) > 0:
			self.dependencies = list()
		for info in infos_deps:
			dep_name = info[1].decode('utf-8')
			dep_pack = Package(dep_name)
			self.dependencies.append(dep_pack)
		# 	depends = True if info[0] == 'DEPENDS' else False
		# 	dep = TagDependency(
		# 		name = Package(info[1].decode('utf-8')).ifwname, 
		# 		version = info[2].decode('utf-8'), 
		# 		depends = depends)
		# 	res.append(dep)
		# self.dependencies =  res

	@classmethod
	def __valid_name(cls, name):
		return name.lower().replace('-', '_').replace(' ', '_').replace('.', '_')