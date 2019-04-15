#!/usr/bin/env python
# -*- coding: utf-8 -*-

from brainvisa.installer.bvi_utils.system import System

from brainvisa.compilation_info import build_directory


class Paths(object):  # pylint: disable=R0903

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
    BVI_SHARE_SCRIPTS = '%s/scripts' % BVI_SHARE

    # BrainVISA Installer files
    BVI_CONFIGURATION = '%s/xml/configuration.xml' % BVI_SHARE

    # Apps
    BV_ENV = 'bv_env'
    BV_ENV_HOST = 'bv_env_host'
    BV_PACKAGING = 'bv_packaging'
    IFW_BINARYCREATOR = 'binarycreator'
    IFW_REPOGEN = 'repogen'
    IFW_ARCHIVEGEN = 'archivegen'
    IFW_DEVTOOL = 'devtool'
    WINEPATH = 'winepath'

    # options
    ARCHIVEGEN_OPTIONS = []

    @staticmethod
    def env_commands(platform):
        """List of environment commands to package for a specific platform
        """
        commands = [Paths.binary_name(Paths.BV_ENV, platform),
                    'bv_env.py',
                    'bv_env.sh',
                    'bv_unenv',
                    'bv_unenv.sh']

        if platform.upper() in (System.Win32, System.Win64):
            commands.append('brainvisa')

        return commands

    @staticmethod
    def binary_extension(platform):
        """Binary extension to use for specific platform, i.e. windows platform
           needs .exe extension
        """
        return '.exe' if platform.upper() in (System.Win32,
                                              System.Win64) else ''

    @staticmethod
    def binary_name(binary, platform):
        """Cross compilation can need specific binary, i.e. windows platform
           needs .exe extension
        """
        ext = Paths.binary_extension(platform)
        if binary.endswith(ext):
            return binary
        return binary + ext
