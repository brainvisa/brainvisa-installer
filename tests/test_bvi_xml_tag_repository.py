#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import xml.etree.ElementTree as ET
from brainvisa.installer.bvi_xml.tag_repository import TagRepository

EXAMPLE1 = """<URL PLATFORM="WIN32">http://localhost/repositories/win32/</URL>"""


EXAMPLE2 = """
<URL 	
PLATFORM="LINUX64" 
USERNAME="Username 0x2849" 
PASSWORD="Password 0x7283"
DISPLAYNAME="Display Name 0xH3HF">
http://localhost/repositories/win32/ 0xJEH34
</URL>"""


def test_TagRepository_init_from_configuration1():
    element = ET.fromstring(EXAMPLE1)
    x = TagRepository()
    x.init_from_configuration(element)
    assert x.Url == 'http://localhost/repositories/win32/'
    assert x.Enabled == '0'
    assert x.Username == None
    assert x.Password == None
    assert x.DisplayName == None


def test_TagRepository_init_from_configuration2():
    element = ET.fromstring(EXAMPLE2)
    x = TagRepository()
    x.init_from_configuration(element)
    assert x.Url == 'http://localhost/repositories/win32/ 0xJEH34'
    assert x.Enabled == '1'
    assert x.Username == 'Username 0x2849'
    assert x.Password == 'Password 0x7283'
    assert x.DisplayName == 'Display Name 0xH3HF'


def test_TagRepository_element1():
    element = ET.fromstring(EXAMPLE1)
    x = TagRepository()
    x.init_from_configuration(element)
    e = x.element
    assert e.tag == 'Repository'
    assert e[0].tag == 'Url'
    assert e[0].text == 'http://localhost/repositories/win32/'
    assert e[1].tag == 'Enabled'
    assert e[1].text == '0'
    assert len(e) == 2


def test_TagRepository_element2():
    element = ET.fromstring(EXAMPLE2)
    x = TagRepository()
    x.init_from_configuration(element)
    e = x.element
    assert e.tag == 'Repository'
    assert e[0].tag == 'Url'
    assert e[0].text == 'http://localhost/repositories/win32/ 0xJEH34'
    assert e[1].tag == 'Enabled'
    assert e[1].text == '1'
    assert e[2].tag == 'Username'
    assert e[2].text == 'Username 0x2849'
    assert e[3].tag == 'Password'
    assert e[3].text == 'Password 0x7283'
    assert e[4].tag == 'DisplayName'
    assert e[4].text == 'Display Name 0xH3HF'
