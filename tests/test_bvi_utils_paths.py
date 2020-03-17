#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import os
from os.path import relpath
from brainvisa.installer.bvi_utils.paths import Paths

FULLPATH = os.path.dirname(os.path.abspath(__file__))
ROOTPATH = "/" + relpath(FULLPATH + "/../.", "/")


def test_bvi_utils_Paths():
    assert Paths.BV == ROOTPATH
    assert Paths.BV_PYTHON == ROOTPATH + '/python'
    assert Paths.BV_SHARE == ROOTPATH + '/share'
    assert Paths.BVI_SHARE == ROOTPATH + '/share/brainvisa/installer'
    assert Paths.BVI_SHARE_XML == ROOTPATH + '/share/brainvisa/installer/xml'
    assert Paths.BVI_SHARE_IMAGES == ROOTPATH + '/share/brainvisa/installer/images'
    assert Paths.BVI_SHARE_LICENSES == ROOTPATH + \
        '/share/brainvisa/installer/licenses'
    assert Paths.BVI_CONFIGURATION == ROOTPATH + \
        '/share/brainvisa/installer/xml/configuration.xml'


@pytest.mark.win32
def test_bvi_utils_Paths_Binary_win():
    assert Paths.BV_ENV == 'bv_env.exe'
    assert Paths.BV_PACKAGING == 'bv_packaging'
    assert Paths.IFW_BINARYCREATOR == 'binarycreator.exe'
    assert Paths.IFW_REPOGEN == 'repogen.exe'
    assert Paths.IFW_ARCHIVEGEN == 'archivegen.exe'


@pytest.mark.linux
def test_bvi_utils_Paths_Binary_linux():
    assert Paths.BV_ENV == 'bv_env'
    assert Paths.BV_PACKAGING == 'bv_packaging'
    assert Paths.IFW_BINARYCREATOR == 'binarycreator'
    assert Paths.IFW_REPOGEN == 'repogen'
    assert Paths.IFW_ARCHIVEGEN == 'archivegen'


@pytest.mark.osx
def test_bvi_utils_Paths_Binary_osx():
    assert Paths.BV_ENV == 'bv_env'
    assert Paths.BV_PACKAGING == 'bv_packaging'
    assert Paths.IFW_BINARYCREATOR == 'binarycreator'
    assert Paths.IFW_REPOGEN == 'repogen'
    assert Paths.IFW_ARCHIVEGEN == 'archivegen'
