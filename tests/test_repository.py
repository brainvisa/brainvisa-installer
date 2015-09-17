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
CURRENTDATE = datetime.datetime.now().strftime("%Y-%m-%d")


def test_Repository_init():
	x = Configuration("%s/in/configuration.xml" % FULLPATH)
	folder = "%s/out/repository" % FULLPATH
	y = Repository(folder, x, None)
	assert y.folder == folder
	assert y.configuration == x
	assert y.date == CURRENTDATE
	assert y.components == None


def test_Repository_mkdir():
	folder_exists = "%s/out/exists" % FULLPATH
	os.mkdir(folder_exists)
	assert os.path.isdir(folder_exists)
	assert Repository._Repository__mkdir(folder_exists) == False
	folder_not_exists =  "%s/out/notexists" % FULLPATH
	assert Repository._Repository__mkdir(folder_not_exists) == True
	assert os.path.isdir(folder_not_exists)


def test_Repository__create_config():
	x = Configuration("%s/in/configuration.xml" % FULLPATH)
	folder = "%s/out/repository" % FULLPATH
	os.mkdir(folder)
	y = Repository(folder, x, None)
	y._Repository__create_config()
	assert os.path.isdir("%s/config" % folder)
	assert os.path.isfile("%s/config/config.xml" % folder)
	z = XmlFile()
	z.read("%s/config/config.xml" % folder)
	assert z.root.find('Name').text == 'BrainVISA Installer'
	assert z.root.find('Version').text == '1.0.0'
	assert z.root.find('Title').text == 'BrainVISA Installer'
	assert z.root.find('Publisher').text == 'CEA IFR49 / I2BM'
	assert z.root.find('ProductUrl').text == 'http://brainvisa.info/'
	rr = z.root.find('RemoteRepositories')
	assert rr[0].find('Url').text == 'http://localhost/repositories/win32/'
	assert rr[3].find('Url').text == 'http://localhost/repositories/linux64/'


def test_Repository__create_packages_app():
	x = Configuration("%s/in/configuration.xml" % FULLPATH)
	folder = "%s/out/repository_pack_app" % FULLPATH
	os.mkdir(folder)
	os.mkdir("%s/packages" % folder)
	y = Repository(folder, x, None)
	y._Repository__create_packages_app()
	filename = '%s/packages/brainvisa.app/meta/package.xml' % folder
	assert os.path.isdir('%s/packages/brainvisa.app' % folder)
	assert os.path.isdir('%s/packages/brainvisa.app/meta' % folder)
	assert os.path.isfile(filename)
	assert '<DisplayName>%s</DisplayName>' % x.category_by_id('APP').Name in open(filename, 'r').read()
	assert '<ReleaseDate>%s</ReleaseDate>' % CURRENTDATE in open(filename, 'r').read()
	assert '<Name>brainvisa.app</Name>' in open(filename, 'r').read()


def test_Repository__create_packages_dev():
	x = Configuration("%s/in/configuration.xml" % FULLPATH)
	folder = "%s/out/repository_pack_dev" % FULLPATH
	os.mkdir(folder)
	os.mkdir("%s/packages" % folder)
	y = Repository(folder, x, None)
	y._Repository__create_packages_dev()
	filename = '%s/packages/brainvisa.dev/meta/package.xml' % folder
	assert os.path.isdir('%s/packages/brainvisa.dev' % folder)
	assert os.path.isdir('%s/packages/brainvisa.dev/meta' % folder)
	assert os.path.isfile(filename)
	assert '<DisplayName>%s</DisplayName>' % x.category_by_id('DEV').Name in open(filename, 'r').read()
	assert '<ReleaseDate>%s</ReleaseDate>' % CURRENTDATE in open(filename, 'r').read()
	assert '<Name>brainvisa.dev</Name>' in open(filename, 'r').read()


def test_Repository__create_packages_thirdparty():
	x = Configuration("%s/in/configuration.xml" % FULLPATH)
	folder = "%s/out/repository_pack_tp" % FULLPATH
	os.mkdir(folder)
	os.mkdir("%s/packages" % folder)
	y = Repository(folder, x, None)
	y._Repository__create_packages_thirdparty()
	filename = '%s/packages/brainvisa.app.thirdparty/meta/package.xml' % folder
	assert os.path.isdir('%s/packages/brainvisa.app.thirdparty' % folder)
	assert os.path.isdir('%s/packages/brainvisa.app.thirdparty/meta' % folder)
	assert os.path.isfile(filename)
	assert '<DisplayName>Thirdparty</DisplayName>' in open(filename, 'r').read()
	assert '<ReleaseDate>%s</ReleaseDate>' % CURRENTDATE in open(filename, 'r').read()
	assert '<Name>brainvisa.app.thirdparty</Name>' in open(filename, 'r').read()
	assert '<Virtual>true</Virtual>' in open(filename, 'r').read()


def test_Repository__create_packages_licenses():
	x = Configuration("%s/in/configuration.xml" % FULLPATH)
	folder = "%s/out/repository_pack_lic" % FULLPATH
	os.mkdir(folder)
	os.mkdir("%s/packages" % folder)
	y = Repository(folder, x, None)
	y._Repository__create_packages_licenses()
	filename = '%s/packages/brainvisa.app.licenses/meta/package.xml' % folder
	assert os.path.isdir('%s/packages/brainvisa.app.licenses' % folder)
	assert os.path.isdir('%s/packages/brainvisa.app.licenses/meta' % folder)
	assert os.path.isfile(filename)
	assert '<DisplayName>Licenses</DisplayName>' in open(filename, 'r').read()
	assert '<ReleaseDate>%s</ReleaseDate>' % CURRENTDATE in open(filename, 'r').read()
	assert '<Name>brainvisa.app.licenses</Name>' in open(filename, 'r').read()
	assert '<Virtual>true</Virtual>' in open(filename, 'r').read()

	assert os.path.isdir('%s/packages/brainvisa.app.licenses.cecill_b' % folder)
	assert os.path.isdir('%s/packages/brainvisa.app.licenses.cecill_b/meta' % folder)
	filename_lic = '%s/packages/brainvisa.app.licenses.cecill_b/meta/package.xml' % folder
	assert os.path.isfile(filename_lic)
	assert os.path.isfile('%s/packages/brainvisa.app.licenses.cecill_b/meta/License_CeCILL-B_V1_en_EN.txt' % folder)
	assert '<License' in open(filename_lic, 'r').read()
	assert 'name="CeCILL-B"' in open(filename_lic, 'r').read()
	assert 'file="License_CeCILL-B_V1_en_EN.txt"' in open(filename_lic, 'r').read()


def test_Repository__create_package_bv_env():
	x = Configuration("%s/in/configuration_script.xml" % FULLPATH)
	folder = "%s/out/repository_pack_bv_env" % FULLPATH
	os.mkdir(folder)
	os.mkdir("%s/packages" % folder)
	y = Repository(folder, x, None)
	y._Repository__create_package_bv_env()
	filename = '%s/packages/brainvisa.app.thirdparty.bv_env/meta/package.xml' % folder
	assert os.path.isdir('%s/packages/brainvisa.app.thirdparty.bv_env/meta' % folder)
	assert os.path.isdir('%s/packages/brainvisa.app.thirdparty.bv_env/data' % folder)
	assert os.path.isfile(filename)
	assert '<Version>1.0</Version>' in open(filename, 'r').read()
	assert '<Name>brainvisa.app.thirdparty.bv_env</Name>' in open(filename, 'r').read()
	assert '<Virtual>true</Virtual>' in open(filename, 'r').read()
	assert os.path.isfile('%s/packages/brainvisa.app.thirdparty.bv_env/data/bin/bv_env.py' % folder)
	assert os.path.isfile('%s/packages/brainvisa.app.thirdparty.bv_env/data/bin/bv_env.sh' % folder)
	assert os.path.isfile('%s/packages/brainvisa.app.thirdparty.bv_env/data/bin/bv_unenv' % folder)
	assert os.path.isfile('%s/packages/brainvisa.app.thirdparty.bv_env/data/bin/bv_unenv.sh' % folder)

	assert os.path.isfile('%s/packages/brainvisa.app.thirdparty.bv_env/meta/script.qs' % folder)


def test_Repository_create():
	x = Configuration()
	y = [Project('soma', x), Project('aims', x), Project('anatomist', x), Project('axon', x)]
	z = Repository(	folder = "%s/out/Repository_Final" % FULLPATH, 
					configuration = x, 
					components = y)
	z.create()