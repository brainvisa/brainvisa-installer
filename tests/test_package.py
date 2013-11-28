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
from brainvisa.compilation_info import packages_info
from brainvisa.compilation_info import packages_dependencies
from brainvisa.compilation_info import build_directory

FULLPATH = os.path.dirname(os.path.abspath(__file__))

def is_package(name):
	path = "%s/out/%s" % (FULLPATH, name)
	assert os.path.isdir(path) 
	assert os.path.isdir('%s/meta' % path)
	assert os.path.isdir('%s/data' % path)
	assert os.path.isfile('%s/meta/package.xml' % path)

def test_Package():
	x = Package(name='axon')
	assert isinstance(x, Package)

def test_Package_dependencies():
	"""'axon': set([('DEPENDS', 'python', '>= 2.7', False),
					('DEPENDS', 'python-qt4', '', False),
					('DEPENDS', 'soma-base', '>= 4.5.0;<< 4.6', False),
					('DEPENDS', 'soma-qtgui', '>= 4.5.0;<< 4.6', False),
					('RECOMMENDS', 'aims-free', '>= 4.5.0;<< 4.6', False),
					('RECOMMENDS', 'brainvisa-share', '>= 4.5.0;<< 4.6', False),
					('RECOMMENDS', 'graphviz', '', False)])
	"""
	x = Package(name='axon')
	deps = x.dependencies
	s_got = set([x.name for x in deps])
	s_expected = set(['python', 'python-qt4', 'soma-base', 'soma-qtgui', 
		'aims-free', 'brainvisa-share', 'graphviz'])
	assert s_got == s_expected
	
	# s2_got = set([x.version for x in deps])
	# s2_expected = set([	'>= 2.7', '', '>= 4.5.0;<< 4.6'])
	# assert s2_got == s2_expected

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
	x.create("%s/out" % FULLPATH)
	assert os.path.isdir('%s/out/brainvisa.app.soma.usrdoc.soma_base_usrdoc' % FULLPATH) 
	assert os.path.isdir('%s/out/brainvisa.app.soma.usrdoc.soma_base_usrdoc/meta' % FULLPATH)
	assert os.path.isdir('%s/out/brainvisa.app.soma.usrdoc.soma_base_usrdoc/data' % FULLPATH)
	assert os.path.isfile('%s/out/brainvisa.app.soma.usrdoc.soma_base_usrdoc/meta/package.xml' % FULLPATH)
	assert os.path.isfile('%s/out/brainvisa.app.soma.usrdoc.soma_base_usrdoc/data/README' % FULLPATH)

	y = XmlFile()
	y.read('%s/out/brainvisa.app.soma.usrdoc.soma_base_usrdoc/meta/package.xml' % FULLPATH)
	assert y.root.find('DisplayName').text == 'Soma-Base-Usrdoc'
	assert y.root.find('Description').text == None
	assert y.root.find('Version').text == '4.5.0'
	assert y.root.find('ReleaseDate').text == datetime.datetime.now().strftime("%Y-%m-%d")
	assert y.root.find('Name').text == 'brainvisa.app.soma.usrdoc.soma_base_usrdoc'
	assert y.root.find('Virtual').text == 'true'
	shutil.rmtree('%s/out/brainvisa.app.soma.usrdoc.soma_base_usrdoc' % FULLPATH)

@pytest.mark.slow
def test_Package_create_with_dependencies():
	x = Package(name='axon')
	x.create("%s/out" % FULLPATH)
	is_package('brainvisa.app.brainvisa_share.run.brainvisa_share')
	is_package('brainvisa.app.soma.run.soma_base')
	is_package('brainvisa.app.soma.run.soma_qtgui')
	is_package('brainvisa.app.thirdparty.blitz++')
	is_package('brainvisa.app.thirdparty.graphviz')
	is_package('brainvisa.app.thirdparty.libcairo2')
	is_package('brainvisa.app.thirdparty.libexpat1')
	is_package('brainvisa.app.thirdparty.libgcc1')
	is_package('brainvisa.app.thirdparty.libgfortran2')
	is_package('brainvisa.app.thirdparty.libjpeg62')
	is_package('brainvisa.app.thirdparty.liblapack3gf')
	is_package('brainvisa.app.thirdparty.libpng12_0')
	is_package('brainvisa.app.thirdparty.libqt4_network')
	is_package('brainvisa.app.thirdparty.libqt4_qt3support')
	is_package('brainvisa.app.thirdparty.libqt4_sql')
	is_package('brainvisa.app.thirdparty.libqt4_xml')
	is_package('brainvisa.app.thirdparty.libqtcore4')
	is_package('brainvisa.app.thirdparty.libqtgui4')
	is_package('brainvisa.app.thirdparty.python')
	is_package('brainvisa.app.thirdparty.python_numpy')
	is_package('brainvisa.app.thirdparty.python_qt4')
	is_package('brainvisa.app.thirdparty.python_sip4')
	is_package('brainvisa.app.thirdparty.zlib')