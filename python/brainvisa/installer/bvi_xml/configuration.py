#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

from brainvisa.installer.bvi_utils.paths import Paths
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

	def category_by_id(self, id_value):
		for cat in self.Categories:
			if cat.Id == id_value:
				return cat
			for subcat in cat.Subcategories:
				if subcat.Id == id_value:
					return subcat
		return None

	def general(self, tag_name):
		"Return the values of <GENERAL> part."
		general = self.root.find('GENERAL')
		elt = general.find(tag_name)
		if elt is None:
			return None
		return elt.text

	@classmethod
	def repositories(cls, element_repositories):
		"Return the values of <REPOSITORIES> part (list of TagRepository objects)."
		res = list()
		for url in element_repositories:
			res.append(TagRepository().init_from_configuration(url))
		return res

	@classmethod
	def licenses(cls, element):
		"Return the values of <LICENSES> part (list of TagLicense objects)."
		res = list()
		for elt_lic in element:
			res.append(TagLicense().init_from_configuration(elt_lic))
		return res

	@classmethod
	def categories(cls, element):
		"Return the values of <CATEGORIES> part (list of TagCategory objects)."
		main_categories = list()
		for cat in element:
			sub_cateogires = list()
			for subcat in cat:
				sub_sub_cateogires = list()
				for subsubcat in subcat:
					sub_sub_cateogires.append(TagCategory().init_from_configuration(subsubcat))
				sub_cateogires.append(
					TagCategory().init_from_configuration(subcat, sub_sub_cateogires))
			main_categories.append(
				TagCategory().init_from_configuration(cat, sub_cateogires))
		return main_categories

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
			InstallerApplicationIcon  		= self.Icon, 
			InstallerWindowIcon  			= self.Icon, 
			Logo 							= self.Icon + '.png', 
			Watermark 						= self.Icon + '.png',
			Banner 							= None, 
			Background 						= None, 
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
			RepositorySettingsPageVisible 	= None, 
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
		self.Uninstallername = self.general('UNINSTALLERNAME')
		self.Allownonasciicharacters = self.general('ALLOWNONASCIICHARACTERS')
		self.Allowspaceinpath = self.general('ALLOWSPACEINPATH')

		reps = self.root.find('REPOSITORIES')
		if reps is not None:
			self.Repositories += self.repositories(reps)

		lics = self.root.find('LICENSES')
		if lics is not None:
			self.Licenses += self.licenses(lics)

		cats = self.root.find('CATEGORIES')
		if cats is not None:
			self.Categories += self.categories(cats)

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
		self.Uninstallername = None
		self.Allownonasciicharacters = None
		self.Allowspaceinpath = None
		self.Repositories = list()
		self.Licenses = list()
		self.Categories = list()

		self.read(filename)
		if alt_filename: 
			self.read(alt_filename)

	

