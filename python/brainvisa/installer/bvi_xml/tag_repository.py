#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

from brainvisa.installer.bvi_utils.system import System


class TagRepository(object):

    """Online repository for the installer.

    Parameters
    ----------
    Url         : url with the list of available components.
    Enabled     : 0 disabling the repository.
    Username      : user on a protected repository.
    Password     : sets the password to use on a protected repository.
    DisplayName : optionally sets a String to display instead of the URL.
    """

    @property
    def element(self):
        e = ET.Element("Repository")
        e_Url = ET.SubElement(e, "Url")
        e_Url.text = self.Url
        if self.Enabled is not None:
            e_Enabled = ET.SubElement(e, "Enabled")
            e_Enabled.text = self.Enabled
        if self.Username is not None:
            e_Username = ET.SubElement(e, "Username")
            e_Username.text = self.Username
        if self.Password is not None:
            e_Password = ET.SubElement(e, "Password")
            e_Password.text = self.Password
        if self.DisplayName is not None:
            e_DisplayName = ET.SubElement(e, "DisplayName")
            e_DisplayName.text = self.DisplayName
        return e

    def __init__(self, Url=None, Enabled=None, Username=None,
                 Password=None, DisplayName=None, Release=None,
                 platform_name=None, private=False):
        self.Url = Url
        self.Enabled = Enabled
        self.Username = Username
        self.Password = Password
        self.DisplayName = DisplayName
        self.PlatformName = platform_name
        self.private = private
        if Release is None:
            try:
                import brainvisa.config  # for release version, depends on axon
                self.Release = brainvisa.config.fullVersion
            except ImportError:
                self.Release = '1.0.0'
        else:
            self.Release = Release

    def init_from_configuration(self, element):
        "Initialize from an XML element from XML configuration file."
        self.Url = element.text.strip()
        self.Url = self.Url.replace('@release@', self.Release)
        self.Url = self.Url.replace('@platform@',
                                    self.PlatformName)
        att_platform = element.attrib.get('PLATFORM')
        self.Enabled = '1' if att_platform is None \
            or System.platform().lower() == att_platform.lower() else '0'
        # att_private = element.attrib.get('PRIVATE')
        # if att_private is not None and att_private in ('1', 'True', 'true'):
           # self.Enabled = '0'
        if self.Url.startswith("file://") and not self.private:
            self.Enabled = '0'
        self.Username = element.attrib.get('USERNAME')
        self.Password = element.attrib.get('PASSWORD')
        self.DisplayName = element.attrib.get('DISPLAYNAME')
        return self
