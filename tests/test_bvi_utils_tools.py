#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import os.path
import shutil
import pytest

from brainvisa.installer.bvi_utils.tools import binarycreator, repogen, archivegen, bv_packaging

FULLPATH = os.path.dirname(os.path.abspath(__file__))


def test_bvi_utils_tools_binarycreator_fullpath_1():
    repository_path = "%s/in/repository" % FULLPATH
    installer_file = "%s/out/only_online_installer" % FULLPATH
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


def test_bvi_utils_tools_binarycreator_fullpath_2():
    repository_path = "%s/in/repository" % FULLPATH
    installer_file = "%s/out/only_offline_installer" % FULLPATH
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


@pytest.mark.xfail
def test_bvi_utils_tools_binarycreator_fullpath_3():
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


def test_bvi_utils_tools_binarycreator_fullpath_4():
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


def test_bvi_utils_tools_repogen():
    path_repository_in = "in/repository"
    path_repository_out = "out/repository_online_x86_64"
    repogen(path_repository_in, path_repository_out)
    assert os.path.isdir(path_repository_out)
    assert os.path.isfile("%s/Updates.xml" % path_repository_out)
    repogen(path_repository_in, path_repository_out, update=True)
    shutil.rmtree(path_repository_out)


def test_bvi_utils_tools_archivegen():
    folder = "in/group"
    archivegen(folder)
    filename = "%s/data.7z" % folder
    assert os.path.isfile(filename)
    os.remove(filename)


def test_bvi_utils_tools_bv_packaging():
    folder = '%s/out/soma_base' % FULLPATH
    bv_packaging('soma-base', 'run', folder)
    assert os.path.isdir(folder)
    assert os.path.isdir("%s/bin" % folder)
    assert os.path.isdir("%s/python" % folder)
    assert os.path.isdir("%s/share" % folder)


def test_bvi_utils_tools_bv_packaging_2():
    folder = '%s/out/soma_base_usrdoc' % FULLPATH
    bv_packaging('soma-base-usrdoc', 'usrdoc', folder)
    assert os.path.isdir(folder)
    assert os.path.isfile("%s/README" % folder)
