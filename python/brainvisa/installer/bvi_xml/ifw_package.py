#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import sys
import xml.etree.ElementTree as ET

import six
from six.moves.html_parser import HTMLParser

from brainvisa.installer.bvi_utils.xml_file import XmlFile


class IFWPackage(XmlFile):  # pylint: disable=R0902

    """Model Qt Installer package.

    Parameters
    ----------
    DisplayName : Human-readable name of the component. Required.
    Description : Human-readable description of the component. Required. Specify translations for the description as values of additional Description tags, with the xml:lang attribute set to the correct locale. If a localization that matches the locale is not found and an untranslated version exists, that one will be used. Otherwise no Description will be shown for that locale.
    Version : Version number of the component in the following format: [0-9]+((.|-)[0-9]+)* such as 1-1; 1.2-2; 3.4.7. Required. If a package needs to show the version number from a child rather than it's own (due to grouping of child packages) one can specify the attribute inheritVersionFrom with the package name the version needs to be inherited from.
    ReleaseDate : Date when this component version was released. Required.
    Name : Domain-like identification for this component. Required.
    TagDependencies : list of dependencies (i.e. TagDependency objects).
    AutoDependOn : Opposite of dependencies. Defines that this component should be loaded if all of the specified components are loaded.
    Virtual : Set to true to hide the component from the installer. Note that setting this on a root component does not work.
    SortingPriority : Priority of the component in the tree. The tree is sorted from highest to lowest priority, with the highest priority on the top.
    TagLicenses : list of licenses (i.e. TagLicense objects).
    Script : File name of a script being loaded. Optional. For more information, see Adding Operations.
    UserInterfaces : List of pages to load. To add several pages, specify several UserInterface sections that each specify the filename of a page. Optional. For more information, see Adding Pages.
    Translations : List of translation files to load. To add several language variants, specify several Translation sections that each specify the filename of a language variant. Optional. For more information, see Translating Pages.
    UpdateText : Description added to the component description if this is an update to the component. Optional.
    Default : Possible values are: true, false, and script. Set to true to preselect the component in the installer. This takes effect only on components that have no visible child components. The boolean values are evaluated directly, while script is resolved during runtime. Add the name of the script as a value of the Script setting in this file.
    Essential : Marks the package as essential to force a restart of the UpdateAgent or MaintenanceTool. This is relevant for updates found with UpdateAgent. If there are updates available for an essential component, the package manager stays disabled until that component is updated. Newly introduced essential components are automatically installed when running the updater.
    ForcedInstallation : Determines that the package must always be installed. End users cannot deselect it in the installer.
    Replaces : Comma-separated list of components to replace. Optional.
    DownloadableArchives : Lists the data files (separated by commas) for an online installer to download. If there is some data inside the component and the package.xml and/or the script has no DownloadableArchives value, the repogen tool registers the found data automatically.
    """

    def update(self, filename):
        "Update the properties in memory."
        self.init('Package')
        root_subelements = {
            'DisplayName': self.DisplayName,
            'Description': self.Description,
            'Version': self.make_valid_version(self.Version),
            'ReleaseDate': self.ReleaseDate,
            'Name':  self.Name,
            'AutoDependOn': self.AutoDependOn,
            'SortingPriority': self.SortingPriority,
            'UpdateText': self.UpdateText,
            'Default': self.Default,
            'Essential': self.Essential,
            'ForcedInstallation': self.ForcedInstallation,
            'Replaces': self.Replaces,
            'DownloadableArchives': self.DownloadableArchives,
            'Script': self.Script,
            'Virtual': None if self.Virtual != 'true' else 'true'

        }
        for name, value in six.iteritems(root_subelements):
            self.set_root_subelement_text(name, value)
        # List subelements
        if self.TagDependencies:
            el = self.add_element('Dependencies')
            el.text = u''
            for i, tl in enumerate(self.TagDependencies):
                text = tl.text
                if sys.version_info[0] <= 2:
                    text = text.decode('utf-8')
                res = text.strip()
                if i < len(self.TagDependencies) - 1:
                    res = res + u', '
                el.text += HTMLParser().unescape(res)
        if self.TagLicenses:
            el = self.add_element('Licenses')
            for tl in self.TagLicenses:
                el.append(tl.element)
        if self.Translations:
            et = self.add_element('Translations')
            for t in self.Translations:
                x = ET.SubElement(et, 'Translation')
                x.text = t
        if self.UserInterfaces:
            eui = self.add_element('UserInterfaces')
            for ui in self.UserInterfaces:
                x = ET.SubElement(eui, 'UserInterface')
                x.text = ui

    def __init__(self,
                 DisplayName=None,
                 Description=None,
                 Version=None,
                 ReleaseDate=None,
                 Name=None,
                 TagDependencies=None,
                 AutoDependOn=None,
                 Virtual=None,
                 SortingPriority=None,
                 TagLicenses=None,
                 Script=None,
                 UserInterfaces=None,
                 Translations=None,
                 UpdateText=None,
                 Default=None,
                 Essential=None,
                 ForcedInstallation=None,
                 Replaces=None,
                 DownloadableArchives=None):
        self.DisplayName = DisplayName
        self.Description = Description
        self.Version = Version
        self.ReleaseDate = ReleaseDate
        self.Name = Name
        self.TagDependencies = TagDependencies
        self.AutoDependOn = AutoDependOn
        self.Virtual = Virtual
        self.SortingPriority = SortingPriority
        self.TagLicenses = TagLicenses
        self.Script = Script
        self.UserInterfaces = UserInterfaces
        self.Translations = Translations
        self.UpdateText = UpdateText
        self.Default = Default
        self.Essential = Essential
        self.ForcedInstallation = ForcedInstallation
        self.Replaces = Replaces
        self.DownloadableArchives = DownloadableArchives

    def make_valid_version(self, version):
        vversion = [c for c in version if c in '.0123456789']
        return ''.join(vversion)
