#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from brainvisa.installer.bvi_utils.paths import Paths

@pytest.mark.specific
def test_bvi_utils_Paths():
	assert Paths.CURRENT == "/home/hakim/Development/CEA/BrainVISA_Installer/05_Repository/brainvisa-installer/trunk/python/brainvisa/installer/bvi_utils"
	assert Paths.BV == '/home/hakim/Development/CEA/BrainVISA_Installer/05_Repository/brainvisa-installer/trunk'
	assert Paths.BVI_CONFIGURATION == '/home/hakim/Development/CEA/BrainVISA_Installer/05_Repository/brainvisa-installer/trunk/share/brainvisa/installer/xml/configuration.xml'
	assert Paths.IFW_REPOGEN == "repogen"
	assert Paths.WIN_EXT == ""