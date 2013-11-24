#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import xml.etree.ElementTree as ET

from brainvisa.installer.bvi_utils.system import System


class TagRepository(object):
	"""Online repository for the installer.

	Parameters
	----------
	Url 		: url with the list of available components.
	Enabled 	: 0 disabling the repository.
	Username  	: user on a protected repository.
	Password 	: sets the password to use on a protected repository.
	DisplayName : optionally sets a String to display instead of the URL.
	"""

	@property
	def element(self):
		e = ET.Element("Repository")
		e_Url = ET.SubElement(e, "Url")
		e_Url.text = self.Url
		if self.Enabled: 
			e_Enabled = ET.SubElement(e, "Enabled")
			e_Enabled.text = self.Enabled
		if self.Username: 
			e_Username = ET.SubElement(e, "Username")
			e_Username.text = self.Username
		if self.Password:
			e_Password = ET.SubElement(e, "Password")
			e_Password.text = self.Password
		if self.DisplayName:
			e_DisplayName = ET.SubElement(e, "DisplayName")
			e_DisplayName.text = self.DisplayName
		return e

	def __init__(self, Url = None, Enabled = None, Username = None, Password = None, DisplayName = None):
		self.Url = Url
		self.Enabled = Enabled
		self.Username = Username
		self.Password = Password
		self.DisplayName = DisplayName

	def init_from_configuration(self, element):
		"Initialize from an XML element from XML configuration file."
		self.Url = element.text.strip()
		self.Enabled = '1' if System.platform() == element.attrib.get('PLATFORM') else '0'
		self.Username = element.attrib.get('USERNAME')
		self.Password = element.attrib.get('PASSWORD')
		self.DisplayName = element.attrib.get('DISPLAYNAME')
		return self