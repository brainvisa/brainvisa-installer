#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import shutil
import os.path
import datetime
from brainvisa.installer.category import Category
from brainvisa.installer.bvi_utils.xml_file import XmlFile
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage

def test_Category():
	x = Category(	
		name='Name 0x9230', 
		description='Description 0xH283', 
		version='1.0', 
		priority='10', 
		virtual='false')
	x.create('test_category')
	assert os.path.isdir('test_category/brainvisa.name_0x9230')
	assert os.path.isdir('test_category/brainvisa.name_0x9230/meta')
	assert os.path.isfile('test_category/brainvisa.name_0x9230/meta/package.xml')
	y = XmlFile()
	y.read('test_category/brainvisa.name_0x9230/meta/package.xml')
	assert y.root.find('DisplayName').text == 'Name 0X9230'
	assert y.root.find('Description').text == 'Description 0xH283'
	assert y.root.find('Version').text == '1.0'
	assert y.root.find('ReleaseDate').text == datetime.datetime.now().strftime("%Y-%m-%d")
	assert y.root.find('Name').text == 'brainvisa.name_0x9230'
	assert y.root.find('Virtual').text == 'false'
	assert y.root.find('SortingPriority').text == '10'
	shutil.rmtree('test_category/brainvisa.name_0x9230')