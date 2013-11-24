#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import shutil

from brainvisa.installer.bvi_utils.tools import binarycreator, repogen, archivegen, bv_packaging

FULLPATH = '/home/hakim/Development/CEA/BrainVISA_Installer/05_Repository/brainvisa-installer/trunk/tests'

def test_bvi_utils_tools_binarycreator_fullpath():
	repository_path = "%s/in/repository" % FULLPATH
	installer_file = "%s/out/offline_installer" % FULLPATH
	binarycreator(installer_file, repository_path, offline_only=True)
	assert os.path.isfile(installer_file)
	os.remove(installer_file)


def test_bvi_utils_tools_binarycreator_relativepath():
	repository_path = "in/repository"
	installer_file = "out/offline_installer"
	binarycreator(installer_file, repository_path, offline_only=True)
	assert os.path.isfile(installer_file)
	os.remove(installer_file)

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
	bv_packaging('soma-base', 'run', 'out/soma_base_test')
	bv_packaging('soma-base-usrdoc', 'usrdoc', 'out/soma_base_usrdoc')
	assert os.path.isdir('out/soma_base_test')
	assert os.path.isdir('out/soma_base_usrdoc')