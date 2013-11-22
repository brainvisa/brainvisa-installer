#!/usr/bin/env python
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET


class TagLicense(object):
	"License."

	@property
	def element(self):
		e = ET.Element('License')
		e.set('name', self.Name)
		e.set('file', self.File)
		return e

	def __init__(self, name = None, file_ = None, version = None, id_ = None):
		self.Id = id_
		self.Name = name
		self.File = file_
		self.Version = version

	def init_from_configuration(self, element):
		"Initialize from an XML element from XML configuration file."
		self.Name = element.attrib.get('NAME')
		self.File = element.attrib.get('FILE')
		self.Version = element.attrib.get('VERSION')
		self.Id = element.attrib.get('ID')
		return self