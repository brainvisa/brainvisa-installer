#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import pprint
import shutil
import os.path
import datetime
from brainvisa.installer.package import Package
from brainvisa.installer.bvi_utils.xml_file import XmlFile
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage
from brainvisa.installer.bvi_xml.tag_dependency import TagDependency
from brainvisa.compilation_info import packages_info, packages_dependencies, build_directory

FOLDER = r'/home/hakim/Development/CEA/BrainVISA/Workpackage/05_Sources/python/brainvisa/installer.test/test_package'

"""
'axon': set([	('DEPENDS', 'python', '>= 2.7', False),
				('DEPENDS', 'python-qt4', '', False),
				('DEPENDS', 'soma-base', '>= 4.5.0;<< 4.6', False),
				('DEPENDS', 'soma-qtgui', '>= 4.5.0;<< 4.6', False),
				('RECOMMENDS', 'aims-free', '>= 4.5.0;<< 4.6', False),
				('RECOMMENDS', 'brainvisa-share', '>= 4.5.0;<< 4.6', False),
				('RECOMMENDS', 'graphviz', '', False)])
"""

def is_package(name):
	path = "test_package/%s" % name
	return os.path.isdir(path) * os.path.isdir('%s/meta' % path) * os.path.isdir('%s/data' % path) * os.path.isfile('%s/meta/package.xml')

def test_Package():
	x = Package(name='axon')
	assert isinstance(x, Package)

def test_Package_dependencies():
	x = Package(name='axon')
	deps = x.dependencies
	s_got = set([	deps[0].Name, 
					deps[1].Name, 
					deps[2].Name, 
					deps[3].Name, 
					deps[4].Name, 
					deps[5].Name, 
					deps[6].Name])
	s_expected = set([	'python', 
						'python-qt4', 
						'soma-base', 
						'soma-qtgui', 
						'aims-free', 
						'brainvisa-share', 
						'graphviz'])
	assert s_got == s_expected
	
	s2_got = set([	deps[0].Version, 
					deps[1].Version, 
					deps[2].Version, 
					deps[3].Version, 
					deps[4].Version, 
					deps[5].Version, 
					deps[6].Version])
	s2_expected = set([	'>= 2.7', 
						'', 
						'>= 4.5.0;<< 4.6'])
	assert s2_got == s2_expected

def test_Package_dependencies_none():
	x = Package(name='soma-base-usrdoc')
	assert x.dependencies == None

def test_Package_ifwname():
	x_run = Package(name='axon')
	x_dev = Package(name='axon-dev')
	x_usrdoc = Package(name='axon-usrdoc')
	x_devdoc = Package(name='axon-devdoc')
	assert x_run.ifwname == 'brainvisa.app.axon.run.axon'
	assert x_dev.ifwname == 'brainvisa.dev.axon.dev.axon_dev'
	assert x_usrdoc.ifwname == 'brainvisa.app.axon.usrdoc.axon_usrdoc'
	assert x_devdoc.ifwname == 'brainvisa.dev.axon.devdoc.axon_devdoc'

def test_Package_create():
	x = Package(name='soma-base-usrdoc')
	x.create(FOLDER)
	assert os.path.isdir(	'test_package/brainvisa.app.soma.usrdoc.soma_base_usrdoc') 
	assert os.path.isdir(	'test_package/brainvisa.app.soma.usrdoc.soma_base_usrdoc/meta')
	assert os.path.isfile('test_package/brainvisa.app.soma.usrdoc.soma_base_usrdoc/meta/package.xml')
	assert os.path.isdir(	'test_package/brainvisa.app.soma.usrdoc.soma_base_usrdoc/data')
	assert os.path.isfile('test_package/brainvisa.app.soma.usrdoc.soma_base_usrdoc/data/soma_base_usrdoc.7z')

	y = XmlFile()
	y.read('test_package/brainvisa.app.soma.usrdoc.soma_base_usrdoc/meta/package.xml')
	assert y.root.find('DisplayName').text == 'Soma-Base-Usrdoc'
	assert y.root.find('Description').text == None
	assert y.root.find('Version').text == '4.5.0'
	assert y.root.find('ReleaseDate').text == datetime.datetime.now().strftime("%Y-%m-%d")
	assert y.root.find('Name').text == 'brainvisa.app.soma.usrdoc.soma_base_usrdoc'
	assert y.root.find('Virtual').text == 'true'
	shutil.rmtree('test_package/brainvisa.app.soma.usrdoc.soma_base_usrdoc')

@pytest.mark.slow
def test_Package_create_with_dependencies():
	x = Package(name='axon')
	x.create(FOLDER)
	assert is_package('brainvisa.app.axon.run.axon')
	assert is_package('brainvisa.app.brainvisa_share.run.brainvisa_share')
	assert is_package('brainvisa.app.soma.run.soma_base')
	assert is_package('brainvisa.app.soma.run.soma_qtgui')
	assert is_package('brainvisa.app.thirdparty.blitz++')
	assert is_package('brainvisa.app.thirdparty.graphviz')
	assert is_package('brainvisa.app.thirdparty.libcairo2')
	assert is_package('brainvisa.app.thirdparty.libexpat1')
	assert is_package('brainvisa.app.thirdparty.libgcc1')
	assert is_package('brainvisa.app.thirdparty.libgfortran2')
	assert is_package('brainvisa.app.thirdparty.libjpeg62')
	assert is_package('brainvisa.app.thirdparty.liblapack3gf')
	assert is_package('brainvisa.app.thirdparty.libltdl7')
	assert is_package('brainvisa.app.thirdparty.libncurses5')
	assert is_package('brainvisa.app.thirdparty.libpng12_0')
	assert is_package('brainvisa.app.thirdparty.libqt4_network')
	assert is_package('brainvisa.app.thirdparty.libqt4_qt3support')
	assert is_package('brainvisa.app.thirdparty.libqt4_sql')
	assert is_package('brainvisa.app.thirdparty.libqt4_xml')
	assert is_package('brainvisa.app.thirdparty.libqtcore4')
	assert is_package('brainvisa.app.thirdparty.libqtgui4')
	assert is_package('brainvisa.app.thirdparty.libreadline5')
	assert is_package('brainvisa.app.thirdparty.libsqlite3_0')
	assert is_package('brainvisa.app.thirdparty.libssl1.0.0')
	assert is_package('brainvisa.app.thirdparty.libstdc++6')
	assert is_package('brainvisa.app.thirdparty.libtiff')
	assert is_package('brainvisa.app.thirdparty.python')
	assert is_package('brainvisa.app.thirdparty.python_numpy')
	assert is_package('brainvisa.app.thirdparty.python_qt4')
	assert is_package('brainvisa.app.thirdparty.python_sip4')
	assert is_package('brainvisa.app.thirdparty.zlib')
	shutil.rmtree('test_package/brainvisa.app.soma.usrdoc.soma_base_usrdoc')