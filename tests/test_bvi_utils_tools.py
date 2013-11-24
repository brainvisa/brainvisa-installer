#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import shutil
import os.path
import os

from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_utils.tools import binarycreator, repogen, archivegen, bv_packaging

OUTPUT = r'/home/hakim/Development/CEA/BrainVISA/Workpackage/05_Sources/python/brainvisa/installer.test/test_bvi_utils_tools'

def test_bvi_utils_tools_binarycreator_offline():
	path_repository = "%s/Repository_Test" % OUTPUT
	path_installer = "%s/offline_installer_test" % OUTPUT
	binarycreator(path_installer, path_repository, offline_only=True)
	assert os.path.isfile(path_installer)
	os.remove(path_installer)

def test_ifw_tools_binarycreator():
	path_repository = "%s/Repository_Test" % OUTPUT
	path_installer = "%s/installer_test" % OUTPUT
	binarycreator(path_installer, path_repository)
	assert os.path.isfile(path_installer)
	os.remove(path_installer)

def test_ifw_tools_repogen():
	path_repository_in = "%s/Repository_Test" % OUTPUT
	path_repository_out = "%s/Repository_Test_Out" % OUTPUT
	repogen(path_repository_in, path_repository_out)
	assert os.path.isdir(path_repository_out)
	# assert os.path.isfile("%s/Updates.xml" % path_repository_out)
	# repogen(path_repository_in, path_repository_out, update=True)
	# shutil.rmtree(path_repository_out)

# def test_tools_archivegen():
# 	folder = "%s/test" % OUTPUT
# 	archivegen(folder)
# 	filename = "%s/data.7z" % folder
# 	assert os.path.isfile(filename)
# 	os.remove("%s" % filename)

# def test_tools_bv_packaging():
# 	folder = OUTPUT
# 	bv_packaging('soma-base', 'run', folder)
# 	#bv_packaging('soma-base-usrdoc', 'usrdoc', folder)