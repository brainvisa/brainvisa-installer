#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Hakim Taklanti"
__copyright__ = "Copyright 2013, CEA / Saclay"
__credits__ = ["Hakim Taklanti", "Yann Cointepas", "Denis Rivière", "Nicolas Souedet"]
__license__ = "CeCILL v2"
__version__ = "0.1"
__maintainer__ = "Hakim Taklanti"
__email__ = "hakim.taklanti@altran.com"
__status__ = "dev"


import os.path
import HTMLParser
import xml.etree.ElementTree as ET
from brainvisa.installer.bvi_utils.xml_file import XmlFile
from brainvisa.installer.bvi_xml.tag_license import TagLicense
from brainvisa.installer.bvi_xml.tag_dependency import TagDependency


class IFWPackage(XmlFile):
	"Model Qt Installer package."

	def update(self, filename):
		"Update the properties in memory."
		self.init('Package')
		# Root subelements
		self.set_root_subelement_text('DisplayName', self.DisplayName)
		self.set_root_subelement_text('Description', self.Description)
		self.set_root_subelement_text('Version', self.Version)
		self.set_root_subelement_text('ReleaseDate', self.ReleaseDate)
		self.set_root_subelement_text('Name', self.Name)
		self.set_root_subelement_text('AutoDependOn', self.AutoDependOn)
		if self.Virtual == 'true':
			self.set_root_subelement_text('Virtual', self.Virtual)
		self.set_root_subelement_text('SortingPriority', self.SortingPriority)
		self.set_root_subelement_text('UpdateText', self.UpdateText)
		self.set_root_subelement_text('Default', self.Default)
		self.set_root_subelement_text('Essential', self.Essential)
		self.set_root_subelement_text('ForcedInstallation', self.ForcedInstallation)
		self.set_root_subelement_text('Replaces', self.Replaces)
		self.set_root_subelement_text('DownloadableArchives', self.DownloadableArchives)
		self.set_root_subelement_text('Script', self.Script)
		# List subelements
		if self.TagDependencies:
			el = self.add_element('Dependencies')
			el.text = u''
			for i, tl in enumerate(self.TagDependencies):
				res = tl.text.decode('utf-8').strip()
				if i < len(self.TagDependencies) - 1:
					res = res + u', '
				el.text += HTMLParser.HTMLParser().unescape(res)
		if self.TagLicenses:
			el = self.add_element('Licenses')
			for tl in self.TagLicenses:
				el.append(tl.element)
		if self.Translations:
			et = self.add_element('Translations')
			for t in self.Translations:
				x = ET.SubElement(et, 'Translation')
				x.text = t
		if self.UserInterfaces:
			eui = self.add_element('UserInterfaces')
			for ui in self.UserInterfaces:
				x = ET.SubElement(eui, 'UserInterface')
				x.text = ui

	def __init__(self, 
		DisplayName = None, 
		Description = None, 
		Version = None, 
		ReleaseDate = None, 
		Name = None, 
		TagDependencies = None, 
		AutoDependOn = None,
		Virtual = None,
		SortingPriority = None,
		TagLicenses = None,
		Script = None,
		UserInterfaces = None,
		Translations = None,
		UpdateText = None,
		Default = None,
		Essential = None,
		ForcedInstallation = None,
		Replaces = None,
		DownloadableArchives = None):
		self.DisplayName = DisplayName
		self.Description = Description
		self.Version = Version
		self.ReleaseDate = ReleaseDate
		self.Name = Name
		self.TagDependencies = TagDependencies
		self.AutoDependOn = AutoDependOn
		self.Virtual = Virtual
		self.SortingPriority = SortingPriority
		self.TagLicenses = TagLicenses
		self.Script = Script
		self.UserInterfaces = UserInterfaces
		self.Translations = Translations
		self.UpdateText = UpdateText
		self.Default = Default
		self.Essential = Essential
		self.ForcedInstallation = ForcedInstallation
		self.Replaces = Replaces
		self.DownloadableArchives = DownloadableArchives