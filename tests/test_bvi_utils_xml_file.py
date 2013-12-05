#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
from brainvisa.installer.bvi_utils.xml_file import XmlFile

FULLPATH = os.path.dirname(os.path.abspath(__file__))

EXAMPLE = r'%s/in/ifw_config_example.xml' % FULLPATH
OUTPUT = r'%s/out/out.xml' % FULLPATH

def test_XmlFile_init():
	x = XmlFile()
	x.init('Installer')
	x.save(OUTPUT)
	del x
	x = XmlFile()
	x.read(OUTPUT)
	assert x.root.tag == 'Installer'

def test_XmlFile_read():
	x = XmlFile()
	x.read(EXAMPLE)
	assert x.root.tag == 'Installer'
	assert x.root[5].text == 'brainvisa_icon'

def test_XmlFile_save():
	x = XmlFile()
	x.read(EXAMPLE)
	assert x.root[5].text == 'brainvisa_icon'
	x.root[5].text = '0x83fdfs83'
	x.save(OUTPUT)
	assert os.path.isfile(OUTPUT)
	del x
	x2 = XmlFile()
	x2.read(OUTPUT)
	assert x2.root[5].text == '0x83fdfs83'

def test_XmlFile_root_subelement():
	x = XmlFile()
	x.read(EXAMPLE)
	n1 = x.root_subelement('AdminTargetDir')
	assert n1.text == '@rootDir@/brainvisa'
	n2 = x.root_subelement('MyNewElement_x24f')
	n2.text = '0x393DS'
	assert n2.text == '0x393DS'
	x.save(OUTPUT)
	del x, n1, n2
	x2 = XmlFile()
	x2.read(OUTPUT)
	e = x2.root_subelement('MyNewElement_x24f')
	assert e.text == '0x393DS'

def test_XmlFile_set_root_subelement_text():
	x = XmlFile()
	x.read(EXAMPLE)
	x.set_root_subelement_text('AdminTargetDir', '0x30432')
	x.save(OUTPUT)
	del x
	x = XmlFile()
	x.read(OUTPUT)
	assert x.root_subelement('AdminTargetDir').text == '0x30432'
	x.set_root_subelement_text('AdminTargetDir', None)
	assert x.root.find('AdminTargetDir') == None

def test_XmlFile_add_element():
	x = XmlFile()
	x.read(EXAMPLE)
	x.add_element('NewElement1', '0x39DD33S')
	x.add_element('NewElement2', '0x3FFDD2S', x.root_subelement('RemoteRepositories'))
	x.save(OUTPUT)
	del x
	x = XmlFile()
	x.read(OUTPUT)
	assert x.root_subelement('NewElement1').text == '0x39DD33S'
	assert x.root_subelement('RemoteRepositories').find('NewElement2').text == '0x3FFDD2S'

def test_XmlFile_element_attribute_value():
	x = XmlFile()
	x.read(EXAMPLE)
	assert x.element_attribute_value('Version', 'inheritVersion') == 'brainvisa.app'
	assert x.element_attribute_value('Repository', 'testAttribute', x.root_subelement('RemoteRepositories')) == '02Xsd2'

def test_XmlFile_set_element_attribute_value():
	x = XmlFile()
	x.read(EXAMPLE)
	x.set_element_attribute_value('Watermark', 'testAttribute2', '0x223FZE2')
	x.save(OUTPUT)
	del x
	x = XmlFile()
	x.read(OUTPUT)
	assert x.element_attribute_value('Watermark', 'testAttribute2') == '0x223FZE2'