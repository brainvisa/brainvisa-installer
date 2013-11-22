#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import shutil
import datetime

from brainvisa.installer.package import Package
from brainvisa.installer.category import Category
from brainvisa.installer.license import License
from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_xml.ifw_config import IFWConfig
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage
from brainvisa.installer.bvi_xml.tag_license import TagLicense


class Repository(object):
	"""BrainVISA Installer repository. It is not the repository for the online 
	installer. It is the temporary repository to build the installer binaries
	and the online repository.

	The destination folder, a Configuration object and a list of components 
	must be specified. The list of components must be Component objects but
	only the Package and Project objects are consistent.
	"""

	def create(self):
		"Create the repository."
		self.mkdir(self.folder)
		self.__create_config()
		self.__create_packages()

	def __init__(self, folder, configuration, components):
		self.folder = folder
		self.configuration = configuration
		now = datetime.datetime.now()
		self.date = now.strftime("%Y-%m-%d")
		self.components = components

	def __mkdir(self, folder):
		"Create the directory and return True if it does not exist, else return false."
		if os.path.isdir(folder):
			return False
		os.mkdir(folder)
		return True

	def __create_config(self):
		f_config = "%s/config" % self.folder
		files = ("logo.png", "logo.ico", "logo.icns", "watermark.png")
		self.__mkdir(f_config)
		for f in files:
			shutil.copyfile("%s/%s" % (Paths.BVI_SHARE_IMAGES, f), "%s/%s" % (f_config, f))
		self.configuration.ifwconfig.save("%s/config.xml" % f_config)

	def __create_packages(self):
		path = "%s/packages" % self.folder
		self.__mkdir(path)
		self.__create_packages_app()
		self.__create_packages_dev()
		self.__create_packages_thirdparty()
		self.__create_packages_licenses()
		for component in self.components:
			component.create(path)

	def __create_packages_app(self):
		path = "%s/packages/brainvisa.app"  % self.folder
		cat = self.configuration.category_by_id('APP')
		p = IFWPackage(	DisplayName = cat.Name, 
						Description = cat.Description, 
						Version = cat.Version, 
						ReleaseDate = self.date, 
						Name = 'brainvisa.app', 
						Virtual = 'false',
						SortingPriority = cat.Priority,
						Default = cat.Default)
		self.__create_package(path, p)

	def __create_packages_dev(self):
		path = "%s/packages/brainvisa.dev"  % self.folder
		cat = self.configuration.category_by_id('DEV')
		p = IFWPackage(	DisplayName = cat.Name, 
						Description = cat.Description, 
						Version = cat.Version, 
						ReleaseDate = self.date, 
						Name = 'brainvisa.dev', 
						Virtual = 'false',
						SortingPriority = cat.Priority,
						Default = cat.Default)
		self.__create_package(path, p)
		
	def __create_packages_thirdparty(self):
		path = "%s/packages/brainvisa.app.thirdparty"  % self.folder
		p = IFWPackage(	DisplayName = 'Thirdparty', 
						Description = 'Thirdparty', 
						Version = '1.0', 
						ReleaseDate = self.date, 
						Name = 'brainvisa.app.thirdparty', 
						Virtual = 'true')
		self.__create_package(path, p)

	def __create_packages_licenses(self):
		path = "%s/packages/brainvisa.app.licenses"  % self.folder
		p = IFWPackage(	DisplayName = 'Licenses', 
						Description = 'Licenses', 
						Version = '1.0', 
						ReleaseDate = self.date, 
						Name = 'brainvisa.app.licenses', 
						Virtual = 'true')
		self.__create_package(path, p)
		for license in self.configuration.Licenses:
			License(license).create("%s/packages" % self.folder)

	def __create_package(self, path, package):
		self.__mkdir(path)
		self.__mkdir("%s/meta" % path)
		package.save("%s/meta/package.xml" % path)


