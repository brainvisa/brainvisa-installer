#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

from brainvisa.installer.bvi_utils.system import System

from brainvisa.compilation_info import build_directory


class Paths(object): #pylint: disable=R0903
	"""Group all paths for the BrainVISA Installer classes."""

	# Utils
	CURRENT = os.path.dirname(os.path.abspath(__file__))

	PATH_SYS = {	System.Win32 : 'win32',
					System.Win64 : 'win64',
					System.Linux32 : 'linux32',
					System.Linux64 : 'linux64',
					System.MacOSX : 'osx'}
	
	WIN_EXT = '.exe' if (
		System.platform() == System.Win32 or 
		System.platform() == System.Win64
	) else ''

	# BrainVISA folders
	BV = build_directory
	BV_BIN = '%s/bin' % BV
	BV_PYTHON = '%s/python' % BV
	BV_SHARE = '%s/share' % BV

	# BrainVISA Installer folders
	BVI_SHARE = '%s/share/brainvisa/installer' % BV
	BVI_SHARE_XML = '%s/xml' % BVI_SHARE
	BVI_SHARE_HTML = '%s/html' % BVI_SHARE
	BVI_SHARE_IMAGES = '%s/images' % BVI_SHARE
	BVI_SHARE_LICENSES = '%s/licenses' % BVI_SHARE
	
	# BrainVISA Installer files
	BVI_CONFIGURATION = '%s/xml/configuration.xml' % BVI_SHARE

	# IFW Binaries
	IFW_BINARYCREATOR 	= 'binarycreator%s' % WIN_EXT
	IFW_REPOGEN 		= 'repogen%s' % WIN_EXT
	IFW_ARCHIVEGEN 		= 'archivegen%s' % WIN_EXT