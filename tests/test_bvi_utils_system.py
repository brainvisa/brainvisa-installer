#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from brainvisa.installer.bvi_utils.system import System


@pytest.mark.specific
def test_System_platform():
	#assert System.platform() == System.Linux64
	#assert System.platform == System.Linux32
	assert System.platform() == System.Win32
	#assert System.platform == System.Win64
	#assert System.platform == System.MacOSX
