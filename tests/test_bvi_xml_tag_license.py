#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from brainvisa.installer.bvi_xml.tag_license import TagLicense

EXAMPLE = """<LICENSE ID="CECILL_2.1" VERSION="2.1" NAME="CeCILL v2.1" FILE="licence_cecill_v2.1_en_en.txt" />"""


def setup_module(module):
	pass

def teardown_module(module):
	pass


def test_TagLicense_init_from_configuration():
	element = ET.fromstring(EXAMPLE)
	x = TagLicense()
	x.init_from_configuration(element)
	assert x.Name == 'CeCILL v2.1'
	assert x.File == 'licence_cecill_v2.1_en_en.txt'
	assert x.Version == '2.1'
	assert x.Id == 'CECILL_2.1'


def test_TagLicense_element():
	x = TagLicense( 'License name 0x923D', 'Filename 0x2389')
	element = x.element
	assert element.tag == 'License'
	assert element.attrib['name'] == 'License name 0x923D'
	assert element.attrib['file'] == 'Filename 0x2389'