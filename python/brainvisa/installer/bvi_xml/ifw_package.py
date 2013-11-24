#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import HTMLParser
import xml.etree.ElementTree as ET

from brainvisa.installer.bvi_utils.xml_file import XmlFile
from brainvisa.installer.bvi_xml.tag_license import TagLicense
from brainvisa.installer.bvi_xml.tag_dependency import TagDependency


class IFWPackage(XmlFile):
	"""Model Qt Installer package.

	Parameters
	----------
	DisplayName : Human-readable name of the component. Required.
	Description : Human-readable description of the component. Required. Specify translations for the description as values of additional Description tags, with the xml:lang attribute set to the correct locale. If a localization that matches the locale is not found and an untranslated version exists, that one will be used. Otherwise no Description will be shown for that locale.
	Version : Version number of the component in the following format: [0-9]+((.|-)[0-9]+)* such as 1-1; 1.2-2; 3.4.7. Required. If a package needs to show the version number from a child rather than it's own (due to grouping of child packages) one can specify the attribute inheritVersionFrom with the package name the version needs to be inherited from.
	ReleaseDate : Date when this component version was released. Required.
	Name : Domain-like identification for this component. Required.
	TagDependencies : list of dependencies (i.e. TagDependency objects).
	AutoDependOn : Opposite of dependencies. Defines that this component should be loaded if all of the specified components are loaded.
	Virtual : Set to true to hide the component from the installer. Note that setting this on a root component does not work.
	SortingPriority : Priority of the component in the tree. The tree is sorted from highest to lowest priority, with the highest priority on the top.
	TagLicenses : list of licenses (i.e. TagLicense objects).
	Script : File name of a script being loaded. Optional. For more information, see Adding Operations.
	UserInterfaces : List of pages to load. To add several pages, specify several UserInterface sections that each specify the filename of a page. Optional. For more information, see Adding Pages.
	Translations : List of translation files to load. To add several language variants, specify several Translation sections that each specify the filename of a language variant. Optional. For more information, see Translating Pages.
	UpdateText : Description added to the component description if this is an update to the component. Optional.
	Default : Possible values are: true, false, and script. Set to true to preselect the component in the installer. This takes effect only on components that have no visible child components. The boolean values are evaluated directly, while script is resolved during runtime. Add the name of the script as a value of the Script setting in this file.
	Essential : Marks the package as essential to force a restart of the UpdateAgent or MaintenanceTool. This is relevant for updates found with UpdateAgent. If there are updates available for an essential component, the package manager stays disabled until that component is updated. Newly introduced essential components are automatically installed when running the updater.
	ForcedInstallation : Determines that the package must always be installed. End users cannot deselect it in the installer.
	Replaces : Comma-separated list of components to replace. Optional.
	DownloadableArchives : Lists the data files (separated by commas) for an online installer to download. If there is some data inside the component and the package.xml and/or the script has no DownloadableArchives value, the repogen tool registers the found data automatically.
	"""

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