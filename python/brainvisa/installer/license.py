#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import shutil
import logging

from brainvisa.installer.component import Component
from brainvisa.installer.bvi_utils.paths import Paths
import brainvisa.installer.bvi_utils.format as ft
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage


class License(Component):

    """BrainVISA Installer license package.

    A BrainVISA package uses the dependency system to configure the license.
    A license component is a virtual package that contains only one license.

    Parameter
    ---------
    taglicense : the license parameters are provided with a TagLicense object.
    """

    @property
    def ifwname(self):
        p_name = ft.ifw_name(self.name)
        return "brainvisa.app.licenses.%s" % p_name

    @property
    def ifwpackage(self):
        package = IFWPackage(
            DisplayName=self.name,
            Description='',
            Version=self.version,
            ReleaseDate=self.date,
            Name=self.ifwname,
            Virtual='true',
            TagLicenses=self.licenses)
        return package

    def create(self, folder):
        if folder in Component.done_created_components \
                or (self.configuration
                    and self.configuration.is_package_excluded(self.name)):
            return
        super(License, self).create(folder)
        src = "%s/%s" % (Paths.BVI_SHARE_LICENSES, self.file)
        dest = "%s/%s/meta/%s" % (folder, self.ifwname, self.file)
        shutil.copyfile(src, dest)

    def __init__(self, taglicense, configuration=None):  # pylint: disable=W0231
        super(License, self).__init__(taglicense.Name,
                                      configuration=configuration)
        self.name = taglicense.Name
        self.project = None
        self.type = None
        self.version = taglicense.Version
        self.licenses = [taglicense]
        self.data = None
        self.file = taglicense.File
        # self.configuration = None
        logging.getLogger().debug("[ BVI ] License: %s" % self.name)
        super(License, self)._Component__init_date()
