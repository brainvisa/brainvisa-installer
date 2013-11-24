#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest

from brainvisa.installer.bvi_utils.bvi_exception import BVIException


def test_valid_projects():
	 with pytest.raises(BVIException) as excinfo:
	 	valid_projects('BadProject')
	 assert excinfo.value.message == BVIException(BVIException.PROJECT_NONEXISTENT, arg).message


def test_valid_names():
	with pytest.raises(BVIException) as excinfo:
		valid_names('BadProject')
	 assert excinfo.value.message == BVIException(BVIException.COMPONENT_NONEXISTENT, arg).message

def test_valid_config():
	with pytest.raises(ValueError) as excinfo:
		valid_config('bad_file.xml')
	 assert excinfo.value.message == "bad_file.xml does not exist!"
