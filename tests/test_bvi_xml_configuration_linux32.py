#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os.path
import pytest
from brainvisa.installer.bvi_xml.configuration import Configuration

FULLPATH = os.path.dirname(os.path.abspath(__file__))
EXAMPLE = r'%s/in/configuration.xml' % FULLPATH


@pytest.mark.linux32
def test_bvi_xml_Configuration_Repostiroy_enabled_linux32():
    x = Configuration(EXAMPLE)
    assert x.Repositories[0].Enabled == '0'  # win32
    assert x.Repositories[1].Enabled == '0'  # osx
    assert x.Repositories[2].Enabled == '1'  # linux32
    assert x.Repositories[3].Enabled == '0'  # linux64


@pytest.mark.linux32
def test_is_packaging_excluded_linux32():
    x = Configuration(EXAMPLE)
    assert x.is_packaging_excluded('anatomist-free') == False
    assert x.is_packaging_excluded('brainvisa-share') == False
    assert x.is_packaging_excluded('libboost') == True


@pytest.mark.linux32
def test_is_package_excluded_linux32():
    x = Configuration(EXAMPLE)
    assert x.is_package_excluded('libboost') == True
