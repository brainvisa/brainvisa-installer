#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ 		= "Hakim Taklanti"
__copyright__ 	= "Copyright 2013, CEA / Saclay"
__credits__ 	= ["Hakim Taklanti", "Yann Cointepas", "Denis Rivière", "Nicolas Souedet"]
__license__ 	= "CeCILL v2"
__version__ 	= "0.1"
__maintainer__ 	= "Hakim Taklanti"
__email__ 		= "hakim.taklanti@altran.com"
__status__ 		= "dev"


import xml.etree.ElementTree as ET
from brainvisa.installer.bvi_xml.ifw_config import IFWConfig
from brainvisa.installer.bvi_xml.tag_repository import TagRepository
from brainvisa.installer.bvi_xml.tag_license import TagLicense
from brainvisa.installer.bvi_xml.tag_category import TagCategory
from brainvisa.installer.bvi_utils.system import System
from brainvisa.installer.bvi_utils.paths import Paths


class Configuration(object):
	"BrainVISA Installer XML Configuration File."

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

	def repositories(self, element_repositories):
		"Return the values of <REPOSITORIES> part (list of TagRepository objects)."
		res = list()
		for url in element_repositories:
			res.append(TagRepository().init_from_configuration(url))
		return res

	def licenses(self, element):
		"Return the values of <LICENSES> part (list of TagLicense objects)."
		res = list()
		for license in element:
			res.append(TagLicense().init_from_configuration(license))
		return res

	def categories(self, element):
		"Return the values of <CATEGORIES> part (list of TagCategory objects)."
		main_categories = list()
		for cat in element:
			sub_cateogires = list()
			for subcat in cat:
				sub_sub_cateogires = list()
				for subsubcat in subcat:
					sub_sub_cateogires.append(TagCategory().init_from_configuration(subsubcat))
				sub_cateogires.append(TagCategory().init_from_configuration(subcat, sub_sub_cateogires))
			main_categories.append(TagCategory().init_from_configuration(cat, sub_cateogires))
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
		self.Repositories = list()
		self.Licenses = list()
		self.Categories = list()

		self.read(filename)
		if alt_filename: 
			self.read(alt_filename)

	

