#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import brainvisa.installer.bvi_utils.format as ft


class TagDependency(object):

    """Model dependency.

    Parameters
    ----------
    name 		: name of dependency.
    version 	: Version number of the component in the following format: [0-9]+((.|-)[0-9]+)* such as 1-1; 1.2-2; 3.4.7.
    comparison  : =, >, <, >= or <=
    depends 	: False if the dependency is optional (this option is not taking into account in this current BrainVISA Installer.)
    """

    @property
    def text(self):
        """Format for the IFW package.xml file. The version numbers is \
        separated by a dash (-).

        The version numbers is defined with a comparison operator (=, >, <, \
        >= or <=).
        """
        separator = '' if self.Version == '' else '-'
        res = "%s%s%s%s" % (
            self.Name, separator, self.Comparison, self.Version)
        res = ft.ifw_version(res)
        res = ft.xml_escape(res)
        return res

    def __init__(self, name, version='', comparison='', depends=True):
        self.Name = name
        self.Version = version
        self.Comparison = comparison
        self.Depends = depends
