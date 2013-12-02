#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import pytest
import xml.etree.ElementTree as ET
from brainvisa.installer.bvi_utils.xml_file import XmlFile
from brainvisa.installer.bvi_xml.ifw_config import IFWConfig
from brainvisa.installer.bvi_xml.configuration import Configuration

FULLPATH = os.path.dirname(os.path.abspath(__file__))

EXAMPLE = r'%s/in/configuration.xml' % FULLPATH
EXAMPLE_PARTIAL = r'%s/in/configuration_partial.xml' % FULLPATH
OUTPUT = r'%s/out/out.xml' % FULLPATH

@pytest.mark.linux
@pytest.mark.linux32
@pytest.mark.win32
@pytest.mark.osx
def test_bvi_xml_Configuration():
	x = Configuration(EXAMPLE)
	assert x.Name == 'BrainVISA Installer'
	assert x.Version == '1.0.0'
	assert x.Title == 'BrainVISA Installer'
	assert x.Publisher == 'CEA IFR49 / I2BM'
	assert x.Producturl == 'http://brainvisa.info/'
	assert x.Targetdir == '@homeDir@/brainvisa'
	assert x.Admintargetdir == '@rootDir@/brainvisa'
	assert x.Uninstallername == 'BrainVISA_Suite-Update'
	assert x.Allownonasciicharacters == 'true'
	assert x.Allowspaceinpath == 'true'

@pytest.mark.linux
@pytest.mark.linux32
@pytest.mark.win32
@pytest.mark.osx
def test_bvi_xml_Configuration_Repostiroy():
	x = Configuration(EXAMPLE)
	assert len(x.Repositories) == 4
	assert x.Repositories[0].Url == 'http://localhost/repositories/win32/'
	assert x.Repositories[1].Url == 'http://localhost/repositories/osx/'
	assert x.Repositories[2].Url == 'http://localhost/repositories/linux32/' 
	assert x.Repositories[3].Url == 'http://localhost/repositories/linux64/'

@pytest.mark.linux
@pytest.mark.linux32
@pytest.mark.win32
@pytest.mark.osx
def test_bvi_xml_Configuration_Repostiroy_exception_by_name():
	x = Configuration(EXAMPLE)
	assert x.exception_by_name('liblapack3gf-0', 'VERSION') == "3.0"
	assert x.exception_by_name('libsqlite3-0', 'VERSION') == "3.7.17"
	assert x.exception_by_name('zeub', 'VERSION') == None
	assert x.exception_by_name('libsqlite3-0', 'VERSIONx') == None


@pytest.mark.linux
@pytest.mark.linux32
@pytest.mark.win32
@pytest.mark.osx
def test_bvi_xml_Configuration_Repostiroy_enabled_linux():
	x = Configuration(EXAMPLE)
	assert x.Repositories[0].Enabled == '0'	# win32
	assert x.Repositories[1].Enabled == '0' # osx
	assert x.Repositories[2].Enabled == '0' # linux32
	assert x.Repositories[3].Enabled == '1' # linux64


@pytest.mark.linux32
def test_bvi_xml_Configuration_Repostiroy_enabled_linux32():
	x = Configuration(EXAMPLE)
	assert x.Repositories[0].Enabled == '0'	# win32
	assert x.Repositories[1].Enabled == '0' # osx
	assert x.Repositories[2].Enabled == '1' # linux32
	assert x.Repositories[3].Enabled == '0' # linux64


@pytest.mark.osx
def test_bvi_xml_Configuration_Repostiroy_enabled_osx():
	x = Configuration(EXAMPLE)
	assert x.Repositories[0].Enabled == '0'	# win32
	assert x.Repositories[1].Enabled == '1' # osx
	assert x.Repositories[2].Enabled == '0' # linux32
	assert x.Repositories[3].Enabled == '0' # linux64


@pytest.mark.win32
def test_bvi_xml_Configuration_Repostiroy_enabled_win32():
	x = Configuration(EXAMPLE)
	assert x.Repositories[0].Enabled == '1'	# win32
	assert x.Repositories[1].Enabled == '0' # osx
	assert x.Repositories[2].Enabled == '0' # linux32
	assert x.Repositories[3].Enabled == '0' # linux64

# def test_bvi_xml_Configuration_Licenses():
# 	"""
# 	<LICENSES>
# 		<LICENSE ID="CECILL_2.1" VERSION="2.1" NAME="CeCILL v2.1" FILE="licence_cecill_v2.1_en_en.txt" />
# 		<LICENSE ID="CECILL_2" VERSION="2.0" NAME="CeCILL v2" FILE="licence_cecill_v2_en_en.txt" />
# 		<LICENSE ID="CECILL_B_1" VERSION="1.0" NAME="CeCILL-B v1" FILE="licence_cecill-b_v1_en_en.txt" />
# 		<LICENSE ID="GPL_3.0" VERSION="3.0" NAME="GPL 3.0" FILE="licence_gpl-3.0_en_en.txt" />
# 		<LICENSE ID="LGPL_3.0" VERSION="3.0" NAME="LGPL 3.0" FILE="licence_lgpl-3.0_en_en.txt" />
# 	</LICENSES>
# 	"""
# 	x = Configuration(EXAMPLE)
# 	assert x.Licenses[0].Id == 'CECILL_2.1'
# 	assert x.Licenses[0].Version == '2.1' 
# 	assert x.Licenses[0].Name == 'CeCILL v2.1' 
# 	assert x.Licenses[0].File == 'licence_cecill_v2.1_en_en.txt'
# 	assert x.Licenses[3].Name == 'GPL 3.0' 

# def test_bvi_xml_Configuration_Categories():
# 	"""
# 	<CATEGORIES>
# 		<CATEGORY NAME="BrainVISA Suite" PRIORITY="10" VERSION="1.0" DESCRIPTION="Description of BrainVISA Suite category">
# 			<CATEGORY NAME="Application" PRIORITY="10" DEFAULT="true">
# 				<CATEGORY ID="run" NAME="Application" PRIORITY="10"/>
# 			</CATEGORY>
# 			<CATEGORY NAME="Documentation" PRIORITY="1">
# 				<CATEGORY ID="usrdoc" NAME="Documentation" />
# 			</CATEGORY> 
# 		</CATEGORY>
# 		<CATEGORY NAME="BrainVISA Development" PRIORITY="1" VERSION="1.0" DESCRIPTION="Description of BrainVISA Development category">
# 			<CATEGORY NAME="Sources" PRIORITY="10">
# 				<CATEGORY ID="devel" NAME="Sources" PRIORITY="10" />
# 			</CATEGORY>
# 			<CATEGORY NAME="Documentation" PRIORITY="1">
# 				<CATEGORY ID="devdoc" NAME="Documentation" PRIORITY="4"/>
# 			</CATEGORY> 
# 		</CATEGORY>
# 	</CATEGORIES>
# 	"""
# 	x = Configuration(EXAMPLE)
# 	assert x.Categories[0].Name == 'BrainVISA Suite'
# 	assert x.Categories[0].Description == 'Description of BrainVISA Suite category'
# 	assert x.Categories[1].Subcategories[0].Name == 'Sources'
# 	assert x.Categories[1].Subcategories[1].Subcategories[0].Id == 'devdoc'

# def test_bvi_xml_Configuration_Alt():
# 	"""
# 	<INSTALLER>
# 		<GENERAL>
# 			<VERSION>2.0.0</VERSION>
# 			<TITLE>BrainVISA Installer 2</TITLE>
# 			<PUBLISHER>CEA 0x829307</PUBLISHER>
# 		</GENERAL>

# 		<REPOSITORIES>
# 			<URL PLATFORM="WIN32">http://localhost/repositories2x08734/win32/</URL>
# 			<URL PLATFORM="LINUX64">http://localhost/repositories2x08734/linux64/</URL>
# 		</REPOSITORIES>

# 		<LICENSES>
# 			<LICENSE ID="License 02.3X.1" VERSION="1.421" NAME="License 02.3X" FILE="licence_cecill_v2.1_en_en.txt" />
# 			<LICENSE ID="License 0x9239" VERSION="2.23" NAME="License 0x9" FILE="licence_cecill_v2_en_en.txt" />
# 		</LICENSES>
# 	</INSTALLER>
# 	"""
# 	x = Configuration(EXAMPLE, EXAMPLE_PARTIAL)
# 	assert x.Version == '2.0.0'
# 	assert x.Title == 'BrainVISA Installer 2'
# 	assert x.Publisher == 'CEA 0x829307'

# def test_bvi_xml_Configuration_Alt_Repositories():
# 	x = Configuration(EXAMPLE, EXAMPLE_PARTIAL)
# 	assert len(x.Repositories) == 6
# 	assert x.Repositories[4].Url == 'http://localhost/repositories2x08734/win32/'
# 	assert x.Repositories[4].Enabled == '0'
# 	assert x.Repositories[5].Url == 'http://localhost/repositories2x08734/linux64/'
# 	assert x.Repositories[5].Enabled == '1'
# 	assert x.Repositories[0].Url == 'http://localhost/repositories/win32/'
# 	assert x.Repositories[0].Enabled == '0'
# 	assert x.Repositories[2].Url == 'http://localhost/repositories/linux32/' 
# 	assert x.Repositories[3].Url == 'http://localhost/repositories/linux64/'
# 	assert x.Repositories[3].Enabled == '1' # OS dependent

# def test_bvi_xml_Configuration_Alt_Licenses():
# 	x = Configuration(EXAMPLE, EXAMPLE_PARTIAL)
# 	assert x.Licenses[0].Id == 'CECILL_2.1'
# 	assert x.Licenses[0].Version == '2.1' 
# 	assert x.Licenses[0].Name == 'CeCILL v2.1' 
# 	assert x.Licenses[0].File == 'licence_cecill_v2.1_en_en.txt'
# 	assert x.Licenses[3].Name == 'GPL 3.0' 
# 	assert len(x.Licenses) == 7
# 	assert x.Licenses[5].Id == 'License 02.3X.1'
# 	assert x.Licenses[6].Name == 'License 0x9'
