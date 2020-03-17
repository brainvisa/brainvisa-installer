#!/usr/bin/env python
# -*- coding: utf-8 -*-

import brainvisa.installer.bvi_utils.format as format


def test_ifw_version():
    assert format.ifw_version('<<\n') == '<'
    assert format.ifw_version('>>\t') == '>'
    assert format.ifw_version(';') == ' '
    assert format.ifw_version('>>>') == '>>'
    assert format.ifw_version('azeaz><<fd ""eds;>>') == 'azeaz><fd ""eds >'
    assert format.ifw_version('fdsfd<s"fds:lg~*$)"') == 'fdsfd<s"fds:lg~*$)"'


def test_ifw_name():
    assert format.ifw_name('library_23930') == 'library_23930'
    assert format.ifw_name('library-323.234') == 'library_323_234'
    assert format.ifw_name('My Library 30283') == 'my_library_30283'
    assert format.ifw_name('lib.lib') == 'lib_lib'
    assert format.ifw_name('LibRary_23930') == 'library_23930'


def test_xml_escape():
    assert format.xml_escape('"') == '&quot;'
    assert format.xml_escape("'") == '&apos;'
    assert format.xml_escape(
        '",\',<,>,&, ') == '&quot;,&apos;,&lt;,&gt;,&amp;,'
    assert format.xml_escape(
        '<BALISE IN THE TEXT>') == '&lt;BALISEINTHETEXT&gt;'
