#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
if sys.version_info[:2] >= (2, 7):
    from html.parser import HTMLParser
else:
    from HTMLParser import HTMLParser
from xml.dom import minidom
import xml.etree.ElementTree as ET


class XmlFile(object):
	"""Utility class for the XML files."""

	def init(self, element_root_name):
		"Intialize the root element with element_root_name."
		self.tree = ET.ElementTree()
		self.root = ET.Element(element_root_name)

	def read(self, filename):
		"Read the XML file and initialize the tree et root element."
		self.tree = ET.parse(filename)
		self.root = self.tree.getroot()	

	def update(self, filename):
		"Abstract: update the internal data."
		pass

	def save(self, filename):
		"Update and the save the XML file."
		self.update(filename)
		with open(filename, 'w') as fo_xml:
			pretty_root	= self.prettify(self.root) 
			fo_xml.write(pretty_root)

	# OBSELETE
	@classmethod
	def prettify(cls, element):
		"Return a pretty-printed XML string for the Element."
		rough_string = ET.tostring(element, 'utf-8')
		reparsed = minidom.parseString(rough_string)
		#return reparsed.toprettyxml(encoding='utf-8')
		pretty = reparsed.toxml(encoding='utf-8')
		if sys.version_info[0] >= 3:
			pretty = pretty.decode('utf-8')
		return pretty

	def base(self, tag_name):
		"Equivalent to root_subelement but if the element does not exist else \
		the function returns None."
		elt = self.root.find(tag_name)
		if elt is None:
			return None
		return elt.text

	def root_subelement(self, element_name):
		"Return a subelement of root. If it does not exist, \
		the subelement is added."
		element = self.root.find(element_name)
		if element is None:
			element = ET.SubElement(self.root, element_name)
		return element

	def set_root_subelement_text(self, element_name, text=None):
		"""Set the text of an element. 

		The element is created if node does not exist.
		The element is deleted if text is None and the element already exists."""
		if text != None:
			element = self.root_subelement(element_name)
			element.text = text
		else:
			element = self.root.find(element_name)
			if not element is None:
				self.root.remove(element)

	def add_element(self, new_element_name, new_element_text=None, 
		parent_element=None):
		"Add and return a element if it does not exist to \
		tree and return it. If element is None, element is equal to root element."
		if parent_element is None: 
			parent_element = self.root
		element = parent_element.find(new_element_name)
		if element is None:
			element = ET.Element(new_element_name)
			parent_element.append(element)
		if new_element_text: 
			element.text = new_element_text
		return element

	def element_attribute_value(self, element_name, attribute_name, 
		parent_element=None):
		"Return the attribute value of node. If node is None, node \
		is equal to root element."
		if parent_element is None: 
			parent_element = self.root
		element = parent_element.find(element_name)
		if element is None:
			return None
		return element.get(attribute_name)

	def set_element_attribute_value(self, element_name, attribute_name, 
		attribute_value, parent_element=None):
		"Set the attribute value. If node is None, node is equal to root element."
		if parent_element is None: 
			parent_element = self.root
		element = parent_element.find(element_name)
		if element is None:
			element = ET.Element(element_name)
			parent_element.append(element)
		element.set(attribute_name, attribute_value)

	def __init__(self):
		self.tree = None
		self.root = None
