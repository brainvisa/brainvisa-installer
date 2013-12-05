#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import shutil
import datetime

from brainvisa.installer.license import License
from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage


class Repository(object):
	"""BrainVISA Installer repository. 

	It is not the repository for the online installer. It is the temporary 
	repository to build the installer binaries and the online repository.

	Parameters
	----------
	folder 			: repository full path (with the repository name).
	configuration 	: Configuration object. 
	components		: list of Component objects. Usually, only the Package 
					  and Project objects are consistent.
	"""

	def create(self):
		"Create the repository."
		self.__mkdir(self.folder)
		self.__create_config()
		self.__create_packages()

	def __init__(self, folder, configuration, components):
		self.folder = folder
		self.configuration = configuration
		now = datetime.datetime.now()
		self.date = now.strftime("%Y-%m-%d")
		self.components = components

	@classmethod
	def __mkdir(cls, folder):
		"Create the directory and return True if it does not exist, else return \
		false."
		if os.path.isdir(folder):
			return False
		os.mkdir(folder)
		return True

	def __create_config(self):
		f_config = "%s/config" % self.folder
		self.__mkdir(f_config)
		for asset in self.configuration.images():
			file_src = "%s/%s" % (Paths.BVI_SHARE_IMAGES, asset)
			file_des = "%s/%s" % (f_config, asset)
			shutil.copyfile(file_src, file_des)
		self.configuration.ifwconfig.save("%s/config.xml" % f_config)

	def __create_packages(self):
		print "[ BVI ]: Create packages..."
		path = "%s/packages" % self.folder
		self.__mkdir(path)
		self.__create_packages_app()
		self.__create_packages_dev()
		self.__create_packages_thirdparty()
		self.__create_packages_licenses()
		self.__create_package_bv_env()
		for component in self.components:
			if self.configuration.is_package_excluded(component.name):
				continue
			component.create(path)

	def __create_packages_app(self):
		print "[ BVI ]: Create Application category..."
		package_name = "brainvisa.app"
		cat = self.configuration.category_by_id('APP')
		self.__create_package(package_name, 
			DisplayName = cat.Name, 
			Description = cat.Description, 
			Version = cat.Version, 
			ReleaseDate = self.date, 
			Name = 'brainvisa.app', 
			Virtual = 'false',
			SortingPriority = cat.Priority,
			Default = cat.Default)

	def __create_packages_dev(self):
		print "[ BVI ]: Create Development category..."
		package_name = "brainvisa.dev"
		cat = self.configuration.category_by_id('DEV')
		self.__create_package(package_name, 
			DisplayName = cat.Name, 
			Description = cat.Description, 
			Version = cat.Version, 
			ReleaseDate = self.date, 
			Name = 'brainvisa.dev', 
			Virtual = 'false',
			SortingPriority = cat.Priority,
			Default = cat.Default)
		
	def __create_packages_thirdparty(self):
		print "[ BVI ]: Create Thirdparty category..."
		package_name = "brainvisa.app.thirdparty"
		self.__create_package(package_name, 
			DisplayName = 'Thirdparty', 
			Description = 'Thirdparty', 
			Version = '1.0', 
			ReleaseDate = self.date, 
			Name = 'brainvisa.app.thirdparty', 
			Virtual = 'true')

	def __create_packages_licenses(self):
		print "[ BVI ]: Create Licenses category..."
		package_name = "brainvisa.app.licenses"
		self.__create_package(package_name,
			DisplayName = 'Licenses', 
			Description = 'Licenses', 
			Version = '1.0', 
			ReleaseDate = self.date, 
			Name = 'brainvisa.app.licenses', 
			Virtual = 'true')
		for tag_license in self.configuration.Licenses:
			License(tag_license).create("%s/packages" % self.folder)

	def __create_package_bv_env(self):
		print "[ BVI ]: Create bv_env package..."
		package_name = "brainvisa.app.thirdparty.bv_env"
		self.__create_package(package_name,
			DisplayName = 'BrainVISA Environment', 
			Description = '', 
			Version = '1.0', 
			ReleaseDate = self.date, 
			Name = 'brainvisa.app.thirdparty.bv_env', 
			Virtual = 'true')
		path_data = "%s/packages/%s/data"  % (self.folder, package_name)
		path_data_bin = "%s/bin" % path_data
		self.__mkdir(path_data)
		self.__mkdir(path_data_bin)
		for cmd in Paths.ENV_COMMANDS:
			file_src = "%s/%s" % (Paths.BV_BIN, cmd)
			file_dest = "%s/%s" % (path_data_bin, cmd)
			shutil.copy(file_src, file_dest)

	def __create_package(self, package_name,
			DisplayName, 
			Description, 
			Version , 
			ReleaseDate, 
			Name, 
			Virtual = None,
			SortingPriority = None,
			Default = None): #pylint: disable=C0103
		package = IFWPackage(	
			DisplayName = DisplayName, 
			Description = Description, 
			Version = Version, 
			ReleaseDate = ReleaseDate, 
			Name = Name, 
			Virtual = Virtual, 
			SortingPriority = SortingPriority,
			Default = Default)
		path = "%s/packages/%s"  % (self.folder, package_name)
		self.__mkdir(path)
		self.__mkdir("%s/meta" % path)
		package.save("%s/meta/package.xml" % path)


