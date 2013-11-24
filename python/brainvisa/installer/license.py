#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import shutil

from brainvisa.installer.component import Component
from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage

from brainvisa.compilation_info import build_directory

class License(Component):
	"""BrainVISA Installer license package.

	A BrainVISA package uses the dependency system to configure the license.
	A license component is a virtual package that contains only one license.

	Parameter
	---------
	taglicense : the license parameters are provided with a TagLicense object.
	"""

	@property
	def ifwname(self):
		p_name = self.name.replace('-', '_').replace(' ', '_').lower()
		return "brainvisa.app.licenses.%s" % p_name

	@property
	def ifwpackage(self):
		package = IFWPackage(
			DisplayName = self.name, 
			Description = '', 
			Version = self.version, 
			ReleaseDate = self.date, 
			Name = self.ifwname, 
			Virtual = 'true',
			TagLicenses = self.licenses)
		return package

	def create(self, folder):
		super(License, self).create(folder)
		src = "%s/%s" % (Paths.BVI_SHARE_LICENSES, self.file)
		dest = "%s/%s/meta/%s" % (folder, self.ifwname, self.file)
		shutil.copyfile(src, dest)

	def __init__(self, taglicense):
		self.name = taglicense.Name
		self.project = None
		self.type = None
		self.version = taglicense.Version
		self.licenses = [taglicense]
		self.data = None
		self.file = taglicense.File
		super(License, self)._Component__init_date()
		