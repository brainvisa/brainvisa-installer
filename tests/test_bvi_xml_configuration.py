#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import xml.etree.ElementTree as ET
from brainvisa.installer.bvi_utils.xml_file import XmlFile
from brainvisa.installer.bvi_xml.ifw_config import IFWConfig
from brainvisa.installer.bvi_xml.configuration import Configuration

FULLPATH = os.path.dirname(os.path.abspath(__file__))

EXAMPLE = r'%s/in/configuration.xml' % FULLPATH
EXAMPLE_SCRIPT = r'%s/in/configuration_script.xml' % FULLPATH
EXAMPLE_PARTIAL = r'%s/in/configuration_partial.xml' % FULLPATH
OUTPUT = r'%s/out/out.xml' % FULLPATH


def test_bvi_xml_Configuration():
	x = Configuration(EXAMPLE)
	assert x.Name == 'BrainVISA Installer'
	assert x.Version == '1.0.0'
	assert x.Title == 'BrainVISA Installer'
	assert x.Publisher == 'CEA IFR49 / I2BM'
	assert x.Producturl == 'http://brainvisa.info/'
	assert x.Targetdir == '@homeDir@/brainvisa'
	assert x.Admintargetdir == '@rootDir@/brainvisa'
	assert x.MaintenanceToolName == 'BrainVISA_Suite-Update'
	assert x.Allownonasciicharacters == 'true'
	assert x.Allowspaceinpath == 'true'


def test_bvi_xml_Configuration_Repostiroy():
	x = Configuration(EXAMPLE)
	assert len(x.Repositories) == 4
	assert x.Repositories[0].Url == 'http://localhost/repositories/win32/'
	assert x.Repositories[1].Url == 'http://localhost/repositories/osx/'
	assert x.Repositories[2].Url == 'http://localhost/repositories/linux32/' 
	assert x.Repositories[3].Url == 'http://localhost/repositories/linux64/'


def test_bvi_xml_Configuration_Repostiroy_exception_by_name():
	x = Configuration(EXAMPLE)
	assert x.exception_info_by_name('liblapack3gf-0', 'VERSION') == "3.0"
	assert x.exception_info_by_name('libsqlite3-0', 'VERSION') == "3.7.17"
	assert x.exception_info_by_name('zeub', 'VERSION') == None
	assert x.exception_info_by_name('libsqlite3-0', 'VERSIONx') == None


def test_is_packaging_excluded():
	x = Configuration(EXAMPLE)
	assert x.is_packaging_excluded('corist') == True
	assert x.is_packaging_excluded('libqt4-multimedia') == True
	assert x.is_packaging_excluded('libsqlite3-0') == False


def test_is_package_excluded():
	x = Configuration(EXAMPLE)
	assert x.is_package_excluded('libqt4-multimedia') == True
	assert x.is_package_excluded('corist') == False
	assert x.is_package_excluded('brainvisa-share') == False
	assert x.is_package_excluded('anatomist-free') == False
	assert x.is_package_excluded('liblapack3gf-0') == False


def test_bvi_xml_Configuration_Licenses():
	x = Configuration(EXAMPLE)
	assert x.Licenses[0].Id == 'CECILL_2.1'
	assert x.Licenses[0].Version == '2.1' 
	assert x.Licenses[0].Name == 'CeCILL v2.1' 
	assert x.Licenses[0].File == 'Licence_CeCILL_V2.1_en_EN.txt'
	assert x.Licenses[3].Name == 'GPL 3.0' 


def test_bvi_xml_Configuration_Categories():
	x = Configuration(EXAMPLE)
	assert x.Categories[0].Name == 'BrainVISA Suite'
	assert x.Categories[0].Description == 'Description of BrainVISA Suite category'
	assert x.Categories[1].Subcategories[0].Name == 'Sources'
	assert x.Categories[1].Subcategories[1].Id == 'devdoc'


def test_bvi_xml_Configuration_Alt():
	x = Configuration(EXAMPLE, EXAMPLE_PARTIAL)
	assert x.Version == '2.0.0'
	assert x.Title == 'BrainVISA Installer 2'
	assert x.Publisher == 'CEA 0x829307'


def test_bvi_xml_Configuration_Alt_Repositories():
	x = Configuration(EXAMPLE, EXAMPLE_PARTIAL)
	assert len(x.Repositories) == 6
	assert x.Repositories[4].Url == 'http://localhost/repositories2x08734/win32/'
	assert x.Repositories[4].Enabled == '0'
	assert x.Repositories[5].Url == 'http://localhost/repositories2x08734/linux64/'
	assert x.Repositories[5].Enabled == '1'
	assert x.Repositories[0].Url == 'http://localhost/repositories/win32/'
	assert x.Repositories[0].Enabled == '0'
	assert x.Repositories[2].Url == 'http://localhost/repositories/linux32/' 
	assert x.Repositories[3].Url == 'http://localhost/repositories/linux64/'
	assert x.Repositories[3].Enabled == '1' # OS dependent


def test_bvi_xml_Configuration_Alt_Licenses():
	x = Configuration(EXAMPLE, EXAMPLE_PARTIAL)
	assert x.Licenses[0].Id == 'CECILL_2.1'
	assert x.Licenses[0].Version == '2.1' 
	assert x.Licenses[0].Name == 'CeCILL v2.1' 
	assert x.Licenses[3].Name == 'GPL 3.0' 
	assert len(x.Licenses) == 7
	assert x.Licenses[5].Id == 'License 02.3X.1'
	assert x.Licenses[6].Name == 'License 0x9'

def test_bvi_xml_Configuration_script_package():
	x = Configuration(EXAMPLE_SCRIPT)
	assert x.script_package('brainvisa.app.thirdparty.bv_env') == 'script_bv_env.js'

def test_bvi_xml_Configuration_script_project():
	x = Configuration(EXAMPLE_SCRIPT)
	assert x.script_project('axon', 'run') == 'script_axon.js'
	assert x.script_project('anatomist', 'run') == 'script_anatomist.js'

