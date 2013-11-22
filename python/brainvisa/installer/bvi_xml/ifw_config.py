#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import xml.etree.ElementTree as ET
from brainvisa.installer.bvi_utils.xml_file import XmlFile
import platform


class IFWConfig(XmlFile):
	"Model of XML IFW config file."

	def update(self, filename):
		self.init('Installer')
		# Root subelements
		self.set_root_subelement_text('Name', self.Name)
		self.set_root_subelement_text('Version', self.Version)
		self.set_root_subelement_text('Title', self.Title)
		self.set_root_subelement_text('Publisher', self.Publisher)
		self.set_root_subelement_text('ProductUrl', self.ProductUrl)
		self.set_root_subelement_text('Icon', self.Icon)
		# if platform.system() != 'Linux:'
		# 	self.set_root_subelement_text('InstallerApplicationIcon', self.InstallerApplicationIcon)
		# self.set_root_subelement_text('InstallerWindowIcon', self.InstallerWindowIcon)
		self.set_root_subelement_text('Logo', self.Logo)
		self.set_root_subelement_text('Watermark', self.Watermark)
		self.set_root_subelement_text('Banner', self.Banner)
		self.set_root_subelement_text('Background', self.Background)
		self.set_root_subelement_text('RunProgram', self.RunProgram)
		self.set_root_subelement_text('RunProgramArguments', self.RunProgramArguments)
		self.set_root_subelement_text('RunProgramDescription', self.RunProgramDescription)
		self.set_root_subelement_text('StartMenuDir', self.StartMenuDir)
		self.set_root_subelement_text('TargetDir', self.TargetDir)
		self.set_root_subelement_text('AdminTargetDir', self.AdminTargetDir)		
		self.set_root_subelement_text('UninstallerName', self.UninstallerName)
		self.set_root_subelement_text('UninstallerIniFile', self.UninstallerIniFile)
		self.set_root_subelement_text('RemoveTargetDir', self.RemoveTargetDir)
		self.set_root_subelement_text('AllowNonAsciiCharacters', self.AllowNonAsciiCharacters)
		self.set_root_subelement_text('RepositorySettingsPageVisible', self.RepositorySettingsPageVisible)
		self.set_root_subelement_text('AllowSpaceInPath', self.AllowSpaceInPath)
		self.set_root_subelement_text('DependsOnLocalInstallerBinary', self.DependsOnLocalInstallerBinary)
		self.set_root_subelement_text('TargetConfigurationFile', self.TargetConfigurationFile)
		self.set_root_subelement_text('Translations', self.Translations)
		self.set_root_subelement_text('UrlQueryString', self.UrlQueryString)
		# List subelements
		if self.TagRepositories:
			e = self.add_element('RemoteRepositories')
			for tr in self.TagRepositories:
				e.append(tr.element)	

	def __init__(self, 
		Name, 
		Version, 
		Title = None, 
		Publisher = None, 
		ProductUrl = None, 
		Icon = None, 
		InstallerApplicationIcon = None, 
		InstallerWindowIcon = None, 
		Logo = None, 
		Watermark = None,
		Banner = None, 
		Background = None, 
		RunProgram = None, 
		RunProgramArguments = None, 
		RunProgramDescription = None, 
		StartMenuDir = None, 
		TargetDir = None, 
		AdminTargetDir = None, 
		TagRepositories = None, 
		UninstallerName = None, 
		UninstallerIniFile = None, 
		RemoveTargetDir = None, 
		AllowNonAsciiCharacters = None, 
		RepositorySettingsPageVisible = None, 
		AllowSpaceInPath = None, 
		DependsOnLocalInstallerBinary = None, 
		TargetConfigurationFile = None, 
		Translations = None,
		UrlQueryString = None):
		self.Name = Name
		self.Version = Version
		self.Title = Title
		self.Publisher = Publisher 
		self.ProductUrl = ProductUrl 
		self.Icon = Icon 
		self.InstallerApplicationIcon = InstallerApplicationIcon 
		self.InstallerWindowIcon = InstallerWindowIcon 
		self.Logo = Logo 
		self.Watermark = Watermark
		self.Banner = Banner 
		self.Background = Background 
		self.RunProgram = RunProgram 
		self.RunProgramArguments = RunProgramArguments 
		self.RunProgramDescription = RunProgramDescription 
		self.StartMenuDir = StartMenuDir 
		self.TargetDir = TargetDir 
		self.AdminTargetDir = AdminTargetDir 
		self.TagRepositories = TagRepositories 
		self.UninstallerName = UninstallerName 
		self.UninstallerIniFile = UninstallerIniFile 
		self.RemoveTargetDir = RemoveTargetDir 
		self.AllowNonAsciiCharacters = AllowNonAsciiCharacters 
		self.RepositorySettingsPageVisible = RepositorySettingsPageVisible 
		self.AllowSpaceInPath = AllowSpaceInPath 
		self.DependsOnLocalInstallerBinary = DependsOnLocalInstallerBinary 
		self.TargetConfigurationFile = TargetConfigurationFile 
		self.Translations = Translations
		self.UrlQueryString = UrlQueryString
