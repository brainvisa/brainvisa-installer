#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
from brainvisa.installer.bvi_utils.system import System

# !!! SPECIFIC PLATFORM TEST !!!
def test_System_platform():
	assert System.platform() == System.Linux64
	#assert System.platform == System.Linux32
	#assert System.platform == System.Win64
	#assert System.platform == System.Win64
	#assert System.platform == System.MacOSX
