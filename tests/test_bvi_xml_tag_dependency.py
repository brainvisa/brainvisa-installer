#!/usr/bin/env python
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as ET
from brainvisa.installer.bvi_xml.tag_dependency import TagDependency


def setup_module(module):
	pass

def teardown_module(module):
	pass


def test_TagDependency_format():
	x = TagDependency('My Dependency')
	assert x.Depends == True
	assert x.format('<< >> ; << >> ;') == '< >   < >  '
	assert x.format('0x2349>>0x23>0R;03') == '0x2349>0x23>0R 03'

def test_TagDependency_text():
	x = TagDependency(
		name = 'My Dep 0x293D2', 
		version= 'Version 0x28UDS', 
		comparison = '>>', 
		depends=False)
	assert x.text == 'My Dep 0x293D2 - > Version 0x28UDS'
	assert x.Depends == False
	assert x.Name == 'My Dep 0x293D2'
	assert x.Comparison == '>>'