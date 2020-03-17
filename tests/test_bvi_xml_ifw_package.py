#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os
import os.path

from brainvisa.installer.bvi_utils.xml_file import XmlFile
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage
from brainvisa.installer.bvi_xml.tag_license import TagLicense
from brainvisa.installer.bvi_xml.tag_dependency import TagDependency

FULLPATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT = r'%s/out/IFWPackage_out.xml' % FULLPATH
OUTPUT2 = r'%s/out/IFWPackage_out2.xml' % FULLPATH


def test_utils_IFWPackage():
    x = IFWPackage(
        DisplayName='DisplayName 0x234',
        Description='Description 0x899',
        Version='Version 0x333',
        ReleaseDate='ReleaseDate 0x893',
        Name='Name 0x689',
        TagDependencies=(
            TagDependency(
                name='Name 0x928',
                version='Version 0xF3E',
                comparison='Comparison 0x288'),
            TagDependency(
                name='Name 0x192',
                version='Version 0x111',
                comparison='Comparison 0x112'),
            TagDependency(
                name='Name 0x109',
                version='Version 0x128',
                comparison='Comparison 0x666')),
        AutoDependOn='AutoDependOn 0x668',
        Virtual='Virtual 0x655',
        SortingPriority='SortingPriority 0x234',
        TagLicenses=(
            TagLicense(
                name='Name 0x23F',
                file_='File 0x11F'),
            TagLicense(
                name='Name 0x897',
                file_='File 0x121'),
            TagLicense(
                name='Name 0x122',
                file_='File 0x001')),
        Script='Script 0x273',
        UserInterfaces=['UserInterfaces 0x6721',
                        'UserInterfaces 0x6722', 'UserInterfaces 0x6723'],
        Translations=['Translations 0x653',
                      'Translations 0x643', 'Translations 0x652'],
        UpdateText='UpdateText 0x672',
        Default='Default 0x772',
        Essential='Essential 0x628',
        ForcedInstallation='ForcedInstallation 0x287',
        Replaces='Replaces 0x577',
        DownloadableArchives='Replaces 0x579')
    x.save(OUTPUT)
    assert os.path.isfile(OUTPUT)
    del x
    x = XmlFile()
    x.read(OUTPUT)
    assert x.root.find('Description').text == 'Description 0x899'
    assert x.root.find('ReleaseDate').text == 'ReleaseDate 0x893'
    assert x.root.find('SortingPriority').text == 'SortingPriority 0x234'
    assert x.root.find('Essential').text == 'Essential 0x628'
    assert x.root.find('Script').text == 'Script 0x273'
    assert x.root.find(
        'Dependencies').text == 'Name0x928-Comparison0x288Version0xF3E, Name0x192-Comparison0x112Version0x111, Name0x109-Comparison0x666Version0x128'
    assert x.root.find('Licenses')[0].attrib['file'] == 'File 0x11F'
    assert x.root.find('Licenses')[2].attrib['name'] == 'Name 0x122'
    assert x.root.find('UserInterfaces')[1].text == 'UserInterfaces 0x6722'
    assert x.root.find('Virtual') == None


def test_utils_IFWPackage_2():
    x = IFWPackage(
        DisplayName='DisplayName 0x38434',
        Virtual='true')
    x.save(OUTPUT)
    assert os.path.isfile(OUTPUT)
    del x
    x = XmlFile()
    x.read(OUTPUT)
    assert x.root.find('DisplayName').text == 'DisplayName 0x38434'
    assert x.root.find('Virtual').text == 'true'
