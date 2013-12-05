#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import pytest
from brainvisa.installer.bvi_xml.configuration import Configuration

FULLPATH = os.path.dirname(os.path.abspath(__file__))
EXAMPLE = r'%s/in/configuration.xml' % FULLPATH


@pytest.mark.linux64
def test_bvi_xml_Configuration_Repostiroy_enabled_linux():
	x = Configuration(EXAMPLE)
	assert x.Repositories[0].Enabled == '0'	# win32
	assert x.Repositories[1].Enabled == '0' # osx
	assert x.Repositories[2].Enabled == '0' # linux32
	assert x.Repositories[3].Enabled == '1' # linux64


@pytest.mark.linux64
def test_is_packaging_excluded_linux64():
	x = Configuration(EXAMPLE)
	assert x.is_packaging_excluded('anatomist-free') == True
	assert x.is_packaging_excluded('brainvisa-share') == False
	assert x.is_packaging_excluded('libboost') == False
	assert x.is_packaging_excluded('soma-qtgui-doc') == False