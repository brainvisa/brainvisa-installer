#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_utils.system import System
from brainvisa.installer.bvi_xml.ifw_config import IFWConfig
from brainvisa.installer.bvi_xml.tag_license import TagLicense
from brainvisa.installer.bvi_xml.tag_category import TagCategory
from brainvisa.installer.bvi_xml.tag_repository import TagRepository


class Configuration(object): #pylint: disable=R0902
	"""BrainVISA Installer XML Configuration File.


	Parameters
	----------
	filename 	 : default configuration XML filename (default Paths.BVI_CONFIGURATION).
	alt_filename : alternative configuration XML filename (default: None). The properties
				   defined in the alternative filename erase the information defined in 
				   the primary filename.
	"""

	def images(self):
		"Return the BVI images (logo, watermark, icon)."
		res = list()
		if self.Logo != None and self.Logo != '':
			res.append(self.Logo)
		if self.Icon != None and self.Icon != '':
			res.append(self.Icon)
		if self.Watermark != None and self.Watermark != '':
			res.append(self.Watermark)
		return res

	def script_package(self, name):
		"Return the name from the package's name."
		return self.__get_script_value(name, 'PACKAGES')

	def script_project(self, name):
		"Return the name from the project's name."
		return self.__get_script_value(name, 'PROJECTS')

	def exception_info_by_name(self, name, param):
		"Return the exception value from name and param."
		exceptions = self.root.find('EXCEPTIONS')
		for exception in exceptions:
			if exception.tag == 'INFO' and \
			exception.attrib.get('NAME') == name and \
			exception.attrib.get('PARAM') == param:
				return exception.attrib.get('VALUE')
		return None

	def is_packaging_excluded(self, name):
		"Return True if the packaging must be excluded."
		exceptions = self.root.find('EXCEPTIONS')
		for exception in exceptions:
			if (exception.tag == 'PACKAGE' and
			exception.attrib.get('NAME') == name and
			(exception.attrib.get('TYPE') == 'PACKAGING' or 
			 exception.attrib.get('TYPE') == 'ALL')):
				platform = exception.attrib.get('PLATFORM')
				if platform:
					if platform != System.platform():
						return False
				return True
		return False

	def is_package_excluded(self, name):
		"Return False if the package must be excluded."
		exceptions = self.root.find('EXCEPTIONS')
		for exception in exceptions:
			if (exception.tag == 'PACKAGE' and
				exception.attrib.get('NAME') == name and 
				exception.attrib.get('TYPE') == 'ALL'):
				platform = exception.attrib.get('PLATFORM')
				if platform:
					if platform != System.platform():
						return False
				return True
		return False

	def category_by_id(self, id_value):
		"Return a TagCategory object from id."
		for cat in self.Categories:
			if cat.Id == id_value:
				return cat
			for subcat in cat.Subcategories:
				if subcat.Id == id_value:
					return subcat
		return None

	def general(self, tag_name):
		"Return the values of <GENERAL> part."
		generals = self.root.find('GENERAL')
		elt = generals.find(tag_name)
		if elt is None:
			return None
		return elt.text

	@property
	def ifwconfig(self):
		"Generate a IFWConfig from configuration file."
		config = IFWConfig(
			Name 							= self.Name, 
			Version 						= self.Version, 
			Title  							= self.Title, 
			Publisher  						= self.Publisher, 
			ProductUrl  					= self.Producturl, 
			Icon  							= None, # Deprecated 
			InstallerApplicationIcon  		= None, # Not portable
			InstallerWindowIcon  			= self.Icon, 
			Logo 							= self.Logo, 
			Watermark 						= self.Watermark,
			Banner 							= None, # Not portable
			Background 						= None, # Not portable
			RunProgram 						= None, 
			RunProgramArguments 			= None, 
			RunProgramDescription 			= None, 
			StartMenuDir 					= 'BrainVISA Suite', 
			TargetDir 						= self.Targetdir, 
			AdminTargetDir 					= self.Admintargetdir, 
			TagRepositories 				= self.Repositories, 
			UninstallerName 				= self.Uninstallername, 
			UninstallerIniFile 				= None, 
			RemoveTargetDir 				= None, 
			AllowNonAsciiCharacters 		= self.Allownonasciicharacters, 
			RepositorySettingsPageVisible 	= None, # Default true
			AllowSpaceInPath 				= self.Allowspaceinpath, 
			DependsOnLocalInstallerBinary 	= None, 
			TargetConfigurationFile 		= None, 
			Translations 					= None,
			UrlQueryString 					= None)
		return config

	def read(self, filename):
		self.tree = ET.parse(filename)
		self.root = self.tree.getroot()
		self.Name = self.general('NAME')
		self.Version = self.general('VERSION')
		self.Title = self.general('TITLE')
		self.Publisher = self.general('PUBLISHER')
		self.Producturl = self.general('PRODUCTURL')
		self.Targetdir = self.general('TARGETDIR')
		self.Admintargetdir = self.general('ADMINTARGETDIR')
		self.Icon = self.general('ICON')
		self.Logo = self.general('LOGO')
		self.Watermark = self.general('WATERMARK')
		self.Uninstallername = self.general('UNINSTALLERNAME')
		self.Allownonasciicharacters = self.general('ALLOWNONASCIICHARACTERS')
		self.Allowspaceinpath = self.general('ALLOWSPACEINPATH')
		self.__init_repositories()
		self.__init_licenses()
		self.__init_categories()

	def __init__(self, filename = Paths.BVI_CONFIGURATION, alt_filename=None):
		"filename is the default configuration file in share, \
		alt_filename is an optional configuration file \
		to override the default configuration."
		self.tree = None
		self.root = None
		self.Name = None
		self.Version = None
		self.Title = None
		self.Publisher = None
		self.Producturl = None
		self.Targetdir = None
		self.Admintargetdir = None
		self.Icon = None
		self.Logo = None
		self.Watermark = None
		self.Uninstallername = None
		self.Allownonasciicharacters = None
		self.Allowspaceinpath = None
		self.Repositories = list()
		self.Licenses = list()
		self.Categories = list()
		self.read(filename)
		if alt_filename is not None: 
			self.read(alt_filename)

	def __init_repositories(self):
		"Return the values of <REPOSITORIES> part (list of TagRepository objects)."
		reps = self.root.find('REPOSITORIES')
		if reps is None:
			return
		for rep in reps:
			self.Repositories.append(TagRepository().init_from_configuration(rep))

	def __init_licenses(self):
		"Return the values of <LICENSES> part (list of TagLicense objects)."
		lics = self.root.find('LICENSES')
		if lics is None:
			return
		for lic in lics:
			self.Licenses.append(TagLicense().init_from_configuration(lic))

	def __init_categories(self):
		"Return the values of <CATEGORIES> part (list of TagCategory objects)."
		cats = self.root.find('CATEGORIES')
		if cats is None:
			return
		for cat in cats:
			sub_cateogires = list()
			for subcat in cat:
				sub_sub_cateogires = list()
				for subsubcat in subcat:
					sub_sub_cateogires.append(TagCategory().init_from_configuration(subsubcat))
				sub_cateogires.append(
					TagCategory().init_from_configuration(subcat, sub_sub_cateogires))
			self.Categories.append(
				TagCategory().init_from_configuration(cat, sub_cateogires))

	def __get_script_value(self, name, tagname):
		"Return the name from the package's name."
		scripts = self.root.find('SCRIPTS')
		for script in scripts:
			if script.tag == tagname:
				for pack in script:
					if pack.attrib.get('NAME') == name:
						return pack.attrib.get('SCRIPT')
		return None