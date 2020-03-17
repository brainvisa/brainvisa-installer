#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import os.path
import shutil
import pytest

from brainvisa.installer.bvi_utils.tools import binarycreator, repogen, archivegen, bv_packaging

FULLPATH = os.path.dirname(os.path.abspath(__file__))


@pytest.mark.win32
def test_bvi_utils_tools_binarycreator_fullpath_1_win():
    repository_path = "%s/in/repository" % FULLPATH
    installer_file = "%s/out/only_offline_installer.exe" % FULLPATH
    online_only = False
    offline_only = True
    exclude = None
    include = None
    binarycreator(
        installer_file,
        repository_path,
        online_only=online_only,
        offline_only=offline_only,
        exclude=exclude,
        include=include)
    assert os.path.isfile(installer_file)
    print("\n[ ! ] ==> Check the binary: %s" % installer_file)


@pytest.mark.win32
def test_bvi_utils_tools_binarycreator_fullpath_2_win():
    repository_path = "%s/in/repository" % FULLPATH
    installer_file = "%s/out/only_online_installer.exe" % FULLPATH
    online_only = False
    offline_only = False
    exclude = None
    include = None
    binarycreator(
        installer_file,
        repository_path,
        online_only=online_only,
        offline_only=offline_only,
        exclude=exclude,
        include=include)
    assert os.path.isfile(installer_file)
    print("\n[ ! ] ==> Check the binary: %s" % installer_file)


@pytest.mark.win32
def test_bvi_utils_tools_binarycreator_fullpath_3_win():
    repository_path = "%s/in/repository" % FULLPATH
    installer_file = "%s/out/only_offline_online_installer" % FULLPATH
    online_only = True
    offline_only = True
    exclude = None
    include = None
    binarycreator(
        installer_file,
        repository_path,
        online_only=online_only,
        offline_only=offline_only,
        exclude=exclude,
        include=include)
    assert os.path.isfile(installer_file)
    print("\n[ ! ] ==> Check the binary: %s" % installer_file)


@pytest.mark.win32
def test_bvi_utils_tools_binarycreator_fullpath_4_win():
    repository_path = "%s/in/repository" % FULLPATH
    installer_file = "%s/out/installer" % FULLPATH
    online_only = False
    offline_only = False
    exclude = None
    include = None
    binarycreator(
        installer_file,
        repository_path,
        online_only=online_only,
        offline_only=offline_only,
        exclude=exclude,
        include=include)
    assert os.path.isfile(installer_file)
    print("\n[ ! ] ==> Check the binary: %s" % installer_file)
