#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from brainvisa.installer.bvi_utils.system import System


@pytest.mark.linux
def test_System_platform_linux64():
    assert System.platform() == System.Linux64


@pytest.mark.linux32
def test_System_platform_linux32():
    assert System.platform() == System.Linux32


@pytest.mark.win32
def test_System_platform_win32():
    assert System.platform() == System.Win32


@pytest.mark.osx
def test_System_platform_osx():
    assert System.platform() == System.MacOSX
