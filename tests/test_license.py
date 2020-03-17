#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import os.path
import datetime

from brainvisa.installer.license import License
from brainvisa.installer.bvi_utils.xml_file import XmlFile
from brainvisa.installer.bvi_xml.tag_license import TagLicense


def test_license_License():
    t = TagLicense(	name="MyLicense",
                    file_='License_CeCILL_V2.1_en_EN.txt',
                    version='3.21',
                    id_="MyID")
    l = License(t)
    l.create('out')
    os.path.isdir('out/brainvisa.app.licenses.mylicense')
    os.path.isdir('out/brainvisa.app.licenses.mylicense/meta')
    os.path.isfile('out/brainvisa.app.licenses.mylicense/meta/package.xml')
    os.path.isfile(
        'out/brainvisa.app.licenses.mylicense/meta/License_CeCILL_V2.1_en_EN.txt')
    x = XmlFile()
    x.read('out/brainvisa.app.licenses.mylicense/meta/package.xml')
    assert x.root.find('DisplayName').text == 'MyLicense'
    assert x.root.find('Description').text == None
    assert x.root.find('Version').text == '3.21'
    assert x.root.find(
        'ReleaseDate').text == datetime.datetime.now().strftime("%Y-%m-%d")
    assert x.root.find('Virtual').text == 'true'
    assert x.root.find('Licenses')[
        0].attrib['file'] == 'License_CeCILL_V2.1_en_EN.txt'
    assert x.root.find('Licenses')[0].attrib['name'] == 'MyLicense'
    shutil.rmtree('out/brainvisa.app.licenses.mylicense')
