#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

from brainvisa.installer.bvi_utils.system import System

from brainvisa.compilation_info import build_directory


class Paths(object): #pylint: disable=R0903
	"""Group all paths for the BrainVISA Installer classes."""

	# BrainVISA folders
	BV = build_directory
	BV_BIN = '%s/bin' % BV
	BV_PYTHON = '%s/python' % BV
	BV_SHARE = '%s/share' % BV

	# BrainVISA Installer folders
	BVI_SHARE = '%s/share/brainvisa/installer' % BV
	BVI_SHARE_XML = '%s/xml' % BVI_SHARE
	BVI_SHARE_IMAGES = '%s/images' % BVI_SHARE
	BVI_SHARE_LICENSES = '%s/licenses' % BVI_SHARE
	
	# BrainVISA Installer files
	BVI_CONFIGURATION = '%s/xml/configuration.xml' % BVI_SHARE

	# Apps
	WIN_EXT = '.exe' if (
		System.platform() == System.Win32 or 
		System.platform() == System.Win64
	) else ''
	BV_ENV 				= 'bv_env%s' % WIN_EXT
	BV_PACKAGING 		= 'bv_packaging'
	IFW_BINARYCREATOR 	= 'binarycreator%s' % WIN_EXT
	IFW_REPOGEN 		= 'repogen%s' % WIN_EXT
	IFW_ARCHIVEGEN 		= 'archivegen%s' % WIN_EXT