#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import datetime

from brainvisa.installer.component import Component
from brainvisa.installer.bvi_xml.configuration import Configuration
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage


FULLPATH = os.path.dirname(os.path.abspath(__file__))
CURRENTDATE = datetime.datetime.now().strftime("%Y-%m-%d")


class ConcreteComponent(Component):

	@property
	def ifwname(self):
		return "ifwname"

	@property
	def ifwpackage(self):
		return IFWPackage()

	def __init__(self, name, data=False, configuration=None):
		super(ConcreteComponent, self).__init__(name, data, configuration)


def test_ConcreteComponent_init():
	x = ConcreteComponent('Name 0x284H', True, None)
	assert x.name 			== 'Name 0x284H'
	assert x.configuration 	== None
	assert x.description 	== ''
	assert x.project 		== ''
	assert x.type 			== 'thirdparty'
	assert x.version 		== '1.0'
	assert x.licenses 		== None
	assert x.virtual 		== 'true'
	assert x.displayname 	== None
	assert x.date 			== CURRENTDATE
	assert x.data 			== True


def test_ConcreteComponent_init_2():
	x = ConcreteComponent('anatomist-gpl', True, None)
	assert x.name 			== 'anatomist-gpl'
	assert x.configuration 	== None
	assert x.description 	== ''
	assert x.project 		== 'anatomist'
	assert x.type 			== 'run'
	assert x.version 		== '4.5.0'
	assert x.licenses 		== ["CeCILL-v2"]
	assert x.virtual 		== 'true'
	assert x.displayname 	== None
	assert x.date 			== CURRENTDATE
	assert x.data 			== True


def test_ConcreteComponent__package_meta_2():
	y = Configuration()
	x = ConcreteComponent('liblapack3gf-0', True, y)
	folder = '%s/out/liblapack3gf_0' % FULLPATH
	os.mkdir(folder)
	x._Component__package_meta(folder)
	assert os.path.isdir("%s/meta" % folder)
	assert os.path.isfile("%s/meta/package.xml" % folder)
	assert x.version == "3.0"


def test_ConcreteComponent__package_meta():
	y = Configuration()
	x = ConcreteComponent('anatomist-gpl', True, y)
	folder = '%s/out/anatomist_gpl' % FULLPATH
	os.mkdir(folder)
	x._Component__package_meta(folder)
	assert os.path.isdir("%s/meta" % folder)
	assert os.path.isfile("%s/meta/package.xml" % folder)


def test_ConcreteComponent__package_data():
	y = Configuration()
	x = ConcreteComponent('axon', True, y)
	folder = '%s/out/axon' % FULLPATH
	os.mkdir(folder)
	x._Component__package_data(folder)
	assert os.path.isdir("%s/data" % folder)
	assert os.path.isdir("%s/data/bin" % folder)
	assert os.path.isdir("%s/data/brainvisa" % folder)
	assert os.path.isdir("%s/data/python" % folder)
	assert os.path.isdir("%s/data/scripts" % folder)
	assert os.path.isdir("%s/data/share" % folder)
	assert os.path.isfile("%s/data/BrainVISA" % folder)
	assert os.path.isfile("%s/data/bin/brainvisa" % folder)


def test_ConcreteComponent__package_data_2():
	y = Configuration("%s/in/configuration.xml" % FULLPATH)
	x = ConcreteComponent('corist', True, y)
	folder = '%s/out/corist' % FULLPATH
	os.mkdir(folder)
	x._Component__package_data(folder)
	assert os.path.isdir("%s/data" % folder) == False


def test_create():
	y = Configuration("%s/in/configuration.xml" % FULLPATH)
	x = ConcreteComponent('soma-io', True, y)
	x.create("%s/out" % FULLPATH)
	assert os.path.isdir("%s/out/ifwname" % FULLPATH)
	assert os.path.isdir("%s/out/ifwname/meta" % FULLPATH)
	assert os.path.isdir("%s/out/ifwname/data" % FULLPATH)
	assert os.path.isdir("%s/out/ifwname/data/bin" % FULLPATH)
	assert os.path.isdir("%s/out/ifwname/data/share" % FULLPATH)
	assert os.path.isfile("%s/out/ifwname/meta/package.xml" % FULLPATH)

	