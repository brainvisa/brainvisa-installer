#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TagCategory(object):  # pylint: disable=R0903

    """Tag Category in BrainVISA Installer XML configuration file.

    Parameters
    ----------
    id_ 		  : type for the subcategories.
    name 		  : name in the component selection page of the installer.
    description   : description in the component selection page of the installer.
    version 	  : version (not taking into account).
    priority 	  : priority of the component in the tree. The tree is sorted from highest to lowest priority, with the highest priority on the top.
    default 	  : set to true to preselect the component in the installer
    subcategories : list of TagCategory objects for the visible subcategories of projects in the installer.
    """

    def __init__(self, id_=None, name=None,
                 description=None, version=None, priority=None,
                 default=None, subcategories=None):
        self.Id = id_
        self.Name = name
        self.Description = description
        self.Version = version
        self.Priority = priority
        self.Default = default
        self.Subcategories = subcategories

    def init_from_configuration(self, element, childs=None):
        "Initialize from an XML element from XML configuration file."
        self.Id = element.attrib.get('ID')
        self.Name = element.attrib.get('NAME')
        self.Description = element.attrib.get('DESCRIPTION')
        self.Version = element.attrib.get('VERSION')
        self.Priority = element.attrib.get('PRIORITY')
        self.Default = element.attrib.get('DEFAULT', 'false')
        self.Subcategories = childs
        return self
