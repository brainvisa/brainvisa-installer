#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from brainvisa.installer.bvi_xml.tag_category import TagCategory

EXAMPLE = """
<CATEGORY NAME="BrainVISA Suite" PRIORITY="10" VERSION="1.0" DESCRIPTION="Description of BrainVISA Suite category">
	<CATEGORY NAME="Application" PRIORITY="10" DEFAULT="true">
		<CATEGORY ID="run" NAME="Application" PRIORITY="10"/>
	</CATEGORY>
	<CATEGORY NAME="Documentation" PRIORITY="1">
		<CATEGORY ID="usrdoc" NAME="Documentation" />
	</CATEGORY> 
</CATEGORY>
"""

def setup_module(module):
	pass

def teardown_module(module):
	pass


def test_TagCategory_init_from_configuration():
	element = ET.fromstring(EXAMPLE)
	x = TagCategory()
	x.init_from_configuration(element, 
		[
			TagCategory().init_from_configuration(element[0], 
				[
					TagCategory().init_from_configuration(element[0][0])
				]
			), 
			TagCategory().init_from_configuration(element[1], 
				[
					TagCategory().init_from_configuration(element[1][0])
				]
			)
		]
	)
	assert x.Id == None
	assert x.Name == 'BrainVISA Suite'
	assert x.Description == 'Description of BrainVISA Suite category'
	assert x.Version == '1.0'
	assert x.Priority == '10'
	assert x.Default == 'false'
	assert len(x.Subcategories) == 2
	assert x.Subcategories[0].Name == 'Application'
	assert x.Subcategories[0].Priority == '10'
	assert x.Subcategories[0].Default == 'true'
	assert x.Subcategories[0].Subcategories[0].Id == 'run'
	assert x.Subcategories[0].Subcategories[0].Name == 'Application'
	assert x.Subcategories[0].Subcategories[0].Priority == '10'
	assert x.Subcategories[1].Subcategories[0].Id == 'usrdoc'