#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pprint
import shutil
import os.path
import datetime

from brainvisa.installer.package import Package
from brainvisa.installer.project import Project
from brainvisa.installer.repository import Repository
from brainvisa.installer.bvi_xml.configuration import Configuration
from brainvisa.installer.bvi_xml.ifw_config import IFWConfig
from brainvisa.installer.bvi_utils.xml_file import XmlFile
from brainvisa.installer.bvi_utils.paths import Paths

FULLPATH = os.path.dirname(os.path.abspath(__file__))

# def test_Repository__create_config():
# 	x = Configuration()
# 	folder = "%s/out/New_Repository" % FULLPATH
# 	os.mkdir(folder)
# 	y = Repository(	name='New_Repository', 
# 					folder='%s/out' % FULLPATH, 
# 					configuration=x, 
# 					components=list())
# 	y._Repository__create_config()
# 	assert os.path.isdir('test_repository/New_Repository/config')
# 	z = XmlFile()
# 	z.read('test_repository/New_Repository/config/config.xml')
# 	assert z.root.find('Name').text == 'BrainVISA Installer'
# 	assert z.root.find('Version').text == '1.0.0'
# 	assert z.root.find('Title').text == 'BrainVISA Installer'
# 	assert z.root.find('Publisher').text == 'CEA IFR49 / I2BM'
# 	assert z.root.find('ProductUrl').text == 'http://brainvisa.info/'
# 	rr = z.root.find('RemoteRepositories')
# 	assert rr[0].find('Url').text == 'http://localhost/repositories/win32/'
# 	assert rr[0].find('Enabled').text == '0'
# 	assert rr[3].find('Url').text == 'http://localhost/repositories/linux64/'
# 	assert rr[3].find('Enabled').text == '1'
# 	shutil.rmtree(folder)

# def test_Repository__create_packages():
# 	x = Configuration(CONFIG)
# 	folder = "test_repository/New_Repository"
# 	os.mkdir(folder)
# 	y = Repository(	name='New_Repository', 
# 					folder='test_repository', 
# 					configuration=x, 
# 					components=list())
# 	y._Repository__create_packages()
	
# 	assert os.path.isdir('test_repository/New_Repository/packages')

# 	assert os.path.isdir('test_repository/New_Repository/packages/brainvisa.app')
# 	assert os.path.isdir('test_repository/New_Repository/packages/brainvisa.app/meta')
# 	a = XmlFile()
# 	a.read('test_repository/New_Repository/packages/brainvisa.app/meta/package.xml')
# 	assert a.root.find('Virtual').text == 'false'
# 	assert a.root.find('DisplayName').text == 'BrainVISA Suite'
	
# 	assert os.path.isdir('test_repository/New_Repository/packages/brainvisa.app.licenses')
# 	assert os.path.isdir('test_repository/New_Repository/packages/brainvisa.app.licenses/meta')
# 	assert os.path.isdir('test_repository/New_Repository/packages/brainvisa.app.licenses.cecill_v2.1')
# 	assert os.path.isdir('test_repository/New_Repository/packages/brainvisa.app.licenses.cecill_v2.1/meta')
# 	b = XmlFile()
# 	b.read('test_repository/New_Repository/packages/brainvisa.app.licenses/meta/package.xml')
# 	assert b.root.find('Virtual').text == 'true'
# 	assert b.root.find('DisplayName').text == 'Licenses'

# 	assert os.path.isdir('test_repository/New_Repository/packages/brainvisa.app.thirdparty')
# 	assert os.path.isdir('test_repository/New_Repository/packages/brainvisa.app.thirdparty/meta')
# 	c = XmlFile()
# 	c.read('test_repository/New_Repository/packages/brainvisa.app.thirdparty/meta/package.xml')
# 	assert c.root.find('Virtual').text == 'true'
# 	assert c.root.find('DisplayName').text == 'Thirdparty'

# 	assert os.path.isdir('test_repository/New_Repository/packages/brainvisa.dev')
# 	assert os.path.isdir('test_repository/New_Repository/packages/brainvisa.dev/meta')
# 	d = XmlFile()
# 	d.read('test_repository/New_Repository/packages/brainvisa.dev/meta/package.xml')
# 	assert d.root.find('Virtual').text == 'false'
# 	assert d.root.find('DisplayName').text == 'BrainVISA Development'
# 	shutil.rmtree(folder)

def test_Repository_create_empty():
	x = Configuration()
	y = list()
	z = Repository(	folder = '%s/out/Repository 0x82F93' % FULLPATH, 
					configuration = x, 
					components = y)
	z.create()

	folders = ( 'Repository_0x82F93',
				'Repository_0x82F93/config',
				'Repository_0x82F93/packages/brainvisa.app',
				'Repository_0x82F93/packages/brainvisa.app/meta',
				'Repository_0x82F93/packages/brainvisa.app.licenses',
				'Repository_0x82F93/packages/brainvisa.app.licenses/meta',
				'Repository_0x82F93/packages/brainvisa.app.thirdparty',
				'Repository_0x82F93/packages/brainvisa.app.thirdparty/meta',
				'Repository_0x82F93/packages/brainvisa.dev',
				'Repository_0x82F93/packages/brainvisa.dev/meta',
				'Repository_0x82F93/packages/brainvisa.app.licenses.cecill_v2.1',
				'Repository_0x82F93/packages/brainvisa.app.licenses.cecill_v2.1/meta')
	files = (	'Repository_0x82F93/packages/brainvisa.app/meta/package.xml',
				'Repository_0x82F93/packages/brainvisa.app.licenses/meta/package.xml',
				'Repository_0x82F93/packages/brainvisa.app.licenses.cecill_v2.1/meta/package.xml')
	
	# for f in folders:
	# 	assert os.path.isdir("%s/out/%s" % (FULLPATH, f))

	# for f in files:
	# 	assert os.path.isfile("%s/out/%s" % (FULLPATH, f))

	#shutil.rmtree('test_repository/Repository_0x82F93')

def test_Repository_create():
	x = Configuration()
	y = [Project('soma', x), Project('aims', x), Project('anatomist', x), Project('axon', x)]
	#y = [Project('soma', x, types = ['run', 'usrdoc'])]
	z = Repository(	folder = "%s/out/Repository_ALL" % FULLPATH, 
					configuration = x, 
					components = y)
	z.create()