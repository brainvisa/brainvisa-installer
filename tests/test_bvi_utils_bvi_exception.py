#!/usr/bin/env python
# -*- coding: utf-8 -*-

from brainvisa.installer.bvi_utils.bvi_exception import BVIException

def test_bvi_utils_BVIException():
	e = BVIException(BVIException.ARCHIVEGEN_FAILED, "0x938303")
	assert e.args[0] == '[ BVI ERROR ] The IFW command repogen failed: 0x938303.'