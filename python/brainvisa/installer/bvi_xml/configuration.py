#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import xml.etree.ElementTree as ET

from brainvisa.installer.bvi_utils.tools import ifw_version
from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_utils.system import System
from brainvisa.installer.bvi_xml.ifw_config import IFWConfig
from brainvisa.installer.bvi_xml.tag_license import TagLicense
from brainvisa.installer.bvi_xml.tag_category import TagCategory
from brainvisa.installer.bvi_xml.tag_repository import TagRepository
import distutils.spawn
import six


class Configuration(object):  # pylint: disable=R0902

    """BrainVISA Installer XML Configuration File.


    Parameters
    ----------
    filename      : default configuration XML filename (default Paths.BVI_CONFIGURATION).
    alt_filename : alternative configuration XML filename (default: None). The properties
                   defined in the alternative filename erase the information defined in
                   the primary filename.
    """

    def images(self):
        "Return the BVI images (logo, watermark, icon)."
        res = list()
        if self.Logo != None and self.Logo != '':
            res.append(self.Logo)
        if self.Icon != None and self.Icon != '':
            res.append(self.Icon)
        if self.Watermark != None and self.Watermark != '':
            res.append(self.Watermark)
        return res

    def script_by_name(self, name):
        "Return the name from the package's name."
        return self.__get_script_value(name, 'PACKAGES')

    def exception_info_by_name(self, name, param):
        "Return the exception value from name and param."
        exceptions = self.root.find('EXCEPTIONS')
        if exceptions is not None:
            for exception in exceptions:
                if exception.tag == 'INFO' and \
                        exception.attrib.get('NAME') == name and \
                        exception.attrib.get('PARAM') == param:
                    platform = exception.attrib.get('PLATFORM')
                    if platform:
                        if platform != System.platform():
                            return None
                    return exception.attrib.get('VALUE')
        return None

    def is_packaging_excluded(self, name):
        "Return True if the packaging must be excluded."
        exceptions = self.root.find('EXCEPTIONS')
        excluded = self.data_packages
        if exceptions is not None:
            for exception in exceptions:
                if (exception.tag == 'PACKAGE' and
                        exception.attrib.get('NAME') == name):
                    platform = exception.attrib.get('PLATFORM')
                    if platform and platform != System.platform():
                        continue
                    etype = exception.attrib.get('TYPE')
                    if etype in ('PACKAGING', 'ALL'):
                        return True
                    if etype == 'DATA_PACKAGE':
                        excluded = not self.data_packages
        return excluded

    def is_package_excluded(self, name):
        "Return False if the package must be excluded."
        exceptions = self.root.find('EXCEPTIONS')
        excluded = self.data_packages
        if exceptions is not None:
            for exception in exceptions:
                if (exception.tag == 'PACKAGE' and
                        exception.attrib.get('NAME') == name):
                    platform = exception.attrib.get('PLATFORM')
                    if platform and platform != System.platform():
                        continue
                    etype = exception.attrib.get('TYPE')
                    if etype == 'DATA_PACKAGE':
                        excluded = not self.data_packages
                    elif etype == 'ALL':
                        return True
        return excluded

    def category_by_id(self, id_value):
        "Return a TagCategory object from id."
        for cat in self.Categories:
            if cat.Id == id_value:
                return cat
            for subcat in cat.Subcategories:
                if subcat.Id == id_value:
                    return subcat
        return None

    def resolve_patterns(self, value):
        try:
            import brainvisa.config  # for release version, depends on axon
            release = brainvisa.config.fullVersion
        except ImportError:
            release = '1.0.0'
        pattern_values = {'release': brainvisa.config.fullVersion,
                          'platform': self.PlatformName}
        for p, v in six.iteritems(pattern_values):
            value = value.replace('@' + p + '@', v)

        return value

    def general(self, tag_name):
        "Return the values of <GENERAL> part."
        generals = self.root.find('GENERAL')
        if generals is not None:
            elt = generals.find(tag_name)
            if elt is None:
                return None
            return elt.text
        return None

    @property
    def ifwconfig(self):
        "Generate a IFWConfig from configuration file."

        config = IFWConfig(
            Name=self.Name,
            Version=self.Version,
            Title=self.Title,
            Publisher=self.Publisher,
            ProductUrl=self.Producturl,
            Icon=None,  # Deprecated
            InstallerApplicationIcon=None,  # Not portable
            InstallerWindowIcon=self.Icon,
            Logo=self.Logo,
            Watermark=self.Watermark,
            Banner=None,  # Not portable
            Background=None,  # Not portable
            RunProgram=None,
            RunProgramArguments=None,
            RunProgramDescription=None,
            StartMenuDir=self.StartMenuDir,
            TargetDir=self.Targetdir,
            AdminTargetDir=self.Admintargetdir,
            TagRepositories=self.Repositories,
            MaintenanceToolName=self.MaintenanceToolName,
            MaintenanceToolIniFile=None,
            RemoveTargetDir=None,
            AllowNonAsciiCharacters=self.Allownonasciicharacters,
            RepositorySettingsPageVisible=None,  # Default true
            AllowSpaceInPath=self.Allowspaceinpath,
            DependsOnLocalInstallerBinary=None,
            TargetConfigurationFile=None,
            Translations=None,
            UrlQueryString=None,
            IFWVersion=self.IFWVersion)

        return config

    def read(self, filename):
        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()
        self.Name = self.resolve_patterns(
            self.general('NAME'))
        self.Version = self.resolve_patterns(
            self.general('VERSION'))
        self.Title = self.resolve_patterns(
            self.general('TITLE'))
        self.Publisher = self.resolve_patterns(
            self.general('PUBLISHER'))
        self.Producturl = self.resolve_patterns(
            self.general('PRODUCTURL'))
        self.Targetdir = self.resolve_patterns(
            self.general('TARGETDIR'))
        self.Admintargetdir = self.resolve_patterns(
            self.general('ADMINTARGETDIR'))
        self.Icon = self.resolve_patterns(
            self.general('ICON'))
        self.Logo = self.resolve_patterns(
            self.general('LOGO'))
        self.Watermark = self.resolve_patterns(
            self.general('WATERMARK'))
        self.StartMenuDir = self.resolve_patterns(
            self.general('STARTMENUDIR'))
        self.MaintenanceToolName = self.resolve_patterns(
            self.general('MAINTENANCETOOLNAME'))
        self.Allownonasciicharacters = self.general('ALLOWNONASCIICHARACTERS')
        self.Allowspaceinpath = self.general('ALLOWSPACEINPATH')
        self.__init_repositories()
        self.__init_licenses()
        self.__init_categories()

    def __init__(self, filename=Paths.BVI_CONFIGURATION, alt_filename=None,
                 release=None, with_dependencies=True, with_thirdparty=True,
                 platform_target=None, platform_name=None, skip_repos=False,
                 skip_repogen=False, skip_existing=False, data_packages=False,
                 private_repos=False, make_options=None,
                 binary_creator_command=None, archivegen_cmd=None,
                 archivegen_opts=[]):
        "filename is the default configuration file in share, \
        alt_filename is an optional configuration file \
        to override the default configuration."
        self.tree = None
        self.root = None
        self.Name = None
        self.Version = None
        self.Title = None
        self.Publisher = None
        self.Producturl = None
        self.Targetdir = None
        self.Admintargetdir = None
        self.Icon = None
        self.Logo = None
        self.Watermark = None
        self.MaintenanceToolName = None
        self.Allownonasciicharacters = None
        self.Allowspaceinpath = None
        self.Repositories = list()
        self.Licenses = list()
        self.Categories = list()
        self.Release = release
        if binary_creator_command:
            self.IFWVersion = ifw_version(binary_creator_command,
                                          platform_target)
        else:
            self.IFWVersion = None

        if platform_name is None:
            platform_name = System.platform().lower()
        self.PlatformName = platform_name
        if platform_target is None:
            platform_target = System.platform().lower()
        self.platform_target = platform_target
        self.make_options = make_options
        self.binary_creator_command = binary_creator_command
        self.archivegen_opts = archivegen_opts
        self.with_dependencies = with_dependencies
        self.with_thirdparty = with_thirdparty
        self.skip_repos = skip_repos
        self.skip_repogen = skip_repogen
        self.skip_existing = skip_existing
        self.data_packages = data_packages
        self.private_repos = private_repos
        self.read(filename)
        if alt_filename is not None:
            self.read(alt_filename)

        if archivegen_cmd is None:
            archivegen_opts = []
            archivegen_cmd = distutils.spawn.find_executable('7z')
            if archivegen_cmd is not None:
                archivegen_opts = ['a']
            else:
                archivegen_cmd = distutils.spawn.find_executable('7za')
                if archivegen_cmd is not None:
                    archivegen_opts = ['a']
                else:
                    archivegen_cmd \
                        = distutils.spawn.find_executable('archivegen')
        # print('archivegen_cmd:', archivegen_cmd)
        # print('archivegen_opts:', archivegen_opts)
        self.archivegen_cmd = archivegen_cmd
        self.archivegen_opts = archivegen_opts
        if self.archivegen_cmd is not None:
            Paths.IFW_ARCHIVEGEN = self.archivegen_cmd
            Paths.ARCHIVEGEN_OPTIONS = self.archivegen_opts

    def __init_repositories(self):
        """Return the values of <REPOSITORIES> part (list of TagRepository
        objects)."""
        reps = self.root.find('REPOSITORIES')
        if reps is None:
            return
        for rep in reps:
            is_private = (rep.attrib.get('PRIVATE', "false")
                          in ("true", "True", "1"))
            if is_private == self.private_repos:
                self.Repositories.append(TagRepository(
                    Release=self.Release,
                    platform_name=self.PlatformName,
                    private=self.private_repos).init_from_configuration(
                        rep))

    def __init_licenses(self):
        "Return the values of <LICENSES> part (list of TagLicense objects)."
        lics = self.root.find('LICENSES')
        if lics is None:
            return
        for lic in lics:
            self.Licenses.append(TagLicense().init_from_configuration(lic))

    def __init_categories(self):
        "Return the values of <CATEGORIES> part (list of TagCategory objects)."
        cats = self.root.find('CATEGORIES')
        if cats is None:
            return
        for cat in cats:
            sub_categories = list()
            for subcat in cat:
                sub_sub_categories = list()
                for subsubcat in subcat:
                    sub_sub_categories.append(
                        TagCategory().init_from_configuration(subsubcat))
                sub_categories.append(
                    TagCategory().init_from_configuration(subcat, sub_sub_categories))
            self.Categories.append(
                TagCategory().init_from_configuration(cat, sub_categories))

    def __get_script_value(self, name, tagname, type_=None):
        "Return the name from the package's name."
        scripts = self.root.find('SCRIPTS')
        if scripts is not None:
            for script in scripts:
                if script.tag == tagname:
                    for pack in script:
                        if pack.attrib.get('NAME') == name:
                            if type_ is None:
                                return pack.attrib.get('SCRIPT')
                            else:
                                if pack.attrib.get('TYPE') == type_:
                                    return pack.attrib.get('SCRIPT')
        return None
