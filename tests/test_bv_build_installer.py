#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import pytest
import argparse

import bv_build_installer

FULLPATH = os.path.dirname(os.path.abspath(__file__))


def test_write_info_package():
    file_dest = "%s/out/write_info_package.txt" % FULLPATH
    component = 'soma-base'
    list_packages = set()
    with open(file_dest, 'w') as fo:
        bv_build_installer.write_info_package(fo, component, list_packages)

    # Soma
    assert '<tr>' in open(file_dest).read()
    assert '<td>soma</td>' in open(file_dest).read()
    assert '<td>soma-base</td>' in open(file_dest).read()
    assert '<td>run</td>' in open(file_dest).read()
    assert '<td>4.5.0</td>' in open(file_dest).read()
    assert '<td>CeCILL-B</td>' in open(file_dest).read()
    assert '</tr>' in open(file_dest).read()

    # Python
    assert '<td>thirdparty</td>' in open(file_dest).read()
    assert '<td>python</td>' in open(file_dest).read()
    assert '<td>thirdparty</td>' in open(file_dest).read()
    assert '<td>2.7.3</td>' in open(file_dest).read()
    assert '<td></td>' in open(file_dest).read()


def test_write_info():
    filename = "%s/out/write_info.txt" % FULLPATH
    projects = ['soma', 'axon']
    names = ['anatomist-free']
    bv_build_installer.write_info(filename, projects, names)
    assert os.path.isfile(filename)

    # Soma
    assert '<tr>' in open(filename).read()
    assert '<td>soma</td>' in open(filename).read()
    assert '<td>soma-base</td>' in open(filename).read()
    assert '<td>run</td>' in open(filename).read()
    assert '<td>4.5.0</td>' in open(filename).read()
    assert '<td>CeCILL-B</td>' in open(filename).read()
    assert '</tr>' in open(filename).read()

    # Python
    assert '<td>thirdparty</td>' in open(filename).read()
    assert '<td>python</td>' in open(filename).read()
    assert '<td>thirdparty</td>' in open(filename).read()
    assert '<td>2.7.3</td>' in open(filename).read()
    assert '<td></td>' in open(filename).read()

    # Anatomist-free
    assert '<td>anatomist-free</td>' in open(filename).read()
    assert '<td>anatomist</td>' in open(filename).read()
    assert '<td>run</td>' in open(filename).read()
    assert '<td>4.5.0</td>' in open(filename).read()
    assert '<td>CeCILL-B</td>' in open(filename).read()

    # Unique occurence
    assert open(filename).read().count('<td>anatomist-free</td>') == 1
    assert open(filename).read().count('<td>python</td>') == 1
    assert open(filename).read().count('<td>soma-base</td>') == 1


def test_valid_config():
    arg = "%s/out/file.xml" % FULLPATH
    open(arg, 'w').close()
    assert bv_build_installer.valid_config(arg) == arg
    arg_fail = "%s/out/file2.xml" % FULLPATH
    with pytest.raises(argparse.ArgumentTypeError) as excinfo:
        bv_build_installer.valid_config(arg_fail)
        assert excinfo.value.message == bv_build_installer.MESSAGE_INVALID_CONFIG % arg_fail


def test_valid_names():
    arg = 'soma-base'
    assert bv_build_installer.valid_names(arg) == arg
    arg_fail = 'soma-base-failed'
    with pytest.raises(argparse.ArgumentTypeError) as excinfo:
        bv_build_installer.valid_names(arg_fail)
        assert excinfo.value.message == bv_build_installer.MESSAGE_INVALID_NAME % arg_fail


def test_valid_projects():
    arg = 'soma'
    assert bv_build_installer.valid_projects(arg) == arg
    arg_fail = 'project_inexistant'
    with pytest.raises(argparse.ArgumentTypeError) as excinfo:
        bv_build_installer.valid_projects(arg_fail)
        assert excinfo.value.message == bv_build_installer.MESSAGE_INVALID_PROJECT % arg_fail
