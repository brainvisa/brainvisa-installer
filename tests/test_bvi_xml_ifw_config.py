#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os.path
from brainvisa.installer.bvi_xml.ifw_config import IFWConfig
from brainvisa.installer.bvi_xml.tag_repository import TagRepository
from brainvisa.installer.bvi_utils.xml_file import XmlFile

OUTPUT = r'out/IFWConfig_out.xml'


def test_utils_IFWConfig():
    x = IFWConfig(
        Name='BrainVISA Suite Installer',
        Version='1.0.0',
        Title='BrainVISA Suite Installer',
        Publisher='CEA IFR49 / I2BM',
        ProductUrl='http://brainvisa.info',
        Icon='brainvisa_icon',
        InstallerApplicationIcon='InstallerApplicationIcon 0x23',
        InstallerWindowIcon='InstallerWindowIcon 0x22',
        Logo='brainvisa_logo.png',
        Watermark='brainvisa_watermark.png',
        Banner='Banner 0x23D',
        Background='Background 0x11',
        RunProgram='RunProgram 0x10',
        RunProgramArguments='RunProgramArguments 0x32',
        RunProgramDescription='RunProgramDescription 0x99',
        StartMenuDir='StartMenuDir 0x77',
        TargetDir='@homeDir@/brainvisa',
        AdminTargetDir='@rootDir@/brainvisa',
        TagRepositories=(
            TagRepository(
                'http://localhost/repositories/linux-x86-64/', '1'),
            TagRepository(
                'http://localhost/repositories/linux-x86-32/', '0'),
            TagRepository('http://localhost/repositories/win32/', '0'),
            TagRepository('http://localhost/repositories/osx/', '0'),
            TagRepository('http://localhost/repositories/test/',
                          '0',
                          'Username 0X32F4',
                          'Password 0x332F',
                          'Display Name 0x2DF3')
        ),
        MaintenanceToolName='BrainVISA_Suite-Update',
        MaintenanceToolIniFile='MaintenanceToolIniFile 0x66',
        RemoveTargetDir='RemoveTargetDir 0x55',
        AllowNonAsciiCharacters='true',
        RepositorySettingsPageVisible='RepositorySettingsPageVisible 0x34',
        AllowSpaceInPath='true',
        DependsOnLocalInstallerBinary='DependsOnLocalInstallerBinary 0x87',
        TargetConfigurationFile='TargetConfigurationFile 0x56',
        Translations='Translations 0x45',
        UrlQueryString='UrlQueryString 0x43')
    x.save(OUTPUT)
    assert os.path.isfile(OUTPUT)
    del x
    x = XmlFile()
    x.read(OUTPUT)
    assert x.root_subelement('Name').text == 'BrainVISA Suite Installer'
    assert x.root_subelement('Version').text == '1.0.0'
    assert x.root_subelement('Title').text == 'BrainVISA Suite Installer'
    assert x.root_subelement('Publisher').text == 'CEA IFR49 / I2BM'
    assert x.root_subelement('ProductUrl').text == 'http://brainvisa.info'
    assert x.root_subelement('Icon').text == 'brainvisa_icon'
    assert x.root_subelement('InstallerApplicationIcon').text == None
    assert x.root_subelement('InstallerWindowIcon').text == None
    assert x.root_subelement('Logo').text == 'brainvisa_logo.png'
    assert x.root_subelement('Watermark').text == 'brainvisa_watermark.png'
    assert x.root_subelement('Banner').text == 'Banner 0x23D'
    assert x.root_subelement('Background').text == 'Background 0x11'
    assert x.root_subelement('RunProgram').text == 'RunProgram 0x10'
    assert x.root_subelement(
        'RunProgramArguments').text == 'RunProgramArguments 0x32'
    assert x.root_subelement(
        'RunProgramDescription').text == 'RunProgramDescription 0x99'
    assert x.root_subelement('StartMenuDir').text == 'StartMenuDir 0x77'
    assert x.root_subelement('TargetDir').text == '@homeDir@/brainvisa'
    assert x.root_subelement('AdminTargetDir').text == '@rootDir@/brainvisa'
    assert x.root_subelement('RemoteRepositories')[
        0][0].text == 'http://localhost/repositories/linux-x86-64/'
    assert x.root_subelement('RemoteRepositories')[0][1].text == '1'
    assert x.root_subelement('RemoteRepositories')[
        1][0].text == 'http://localhost/repositories/linux-x86-32/'
    assert x.root_subelement('RemoteRepositories')[1][1].text == '0'
    assert x.root_subelement('RemoteRepositories')[
        2][0].text == 'http://localhost/repositories/win32/'
    assert x.root_subelement('RemoteRepositories')[2][1].text == '0'
    assert x.root_subelement('RemoteRepositories')[
        3][0].text == 'http://localhost/repositories/osx/'
    assert x.root_subelement('RemoteRepositories')[3][1].text == '0'
    assert x.root_subelement('RemoteRepositories')[
        4][0].text == 'http://localhost/repositories/test/'
    assert x.root_subelement('RemoteRepositories')[4][1].text == '0'
    assert x.root_subelement('RemoteRepositories')[
        4][2].text == 'Username 0X32F4'
    assert x.root_subelement('RemoteRepositories')[
        4][3].text == 'Password 0x332F'
    assert x.root_subelement('RemoteRepositories')[
        4][4].text == 'Display Name 0x2DF3'
    assert x.root_subelement(
        'MaintenanceToolName').text == 'BrainVISA_Suite-Update'
    assert x.root_subelement(
        'MaintenanceToolIniFile').text == 'MaintenanceToolIniFile 0x66'
    assert x.root_subelement('RemoveTargetDir').text == 'RemoveTargetDir 0x55'
    assert x.root_subelement('AllowNonAsciiCharacters').text == 'true'
    assert x.root_subelement(
        'RepositorySettingsPageVisible').text == 'RepositorySettingsPageVisible 0x34'
    assert x.root_subelement('AllowSpaceInPath').text == 'true'
    assert x.root_subelement(
        'DependsOnLocalInstallerBinary').text == 'DependsOnLocalInstallerBinary 0x87'
    assert x.root_subelement(
        'TargetConfigurationFile').text == 'TargetConfigurationFile 0x56'
    assert x.root_subelement('Translations').text == 'Translations 0x45'
    assert x.root_subelement('UrlQueryString').text == 'UrlQueryString 0x43'
