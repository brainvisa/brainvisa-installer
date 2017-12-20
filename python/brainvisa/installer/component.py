#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import abc
import shutil
import glob
import datetime
import os.path
import logging

from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_utils.tools import bv_packaging
from brainvisa.installer.bvi_utils.tools import archivegen

from brainvisa.compilation_info import packages_info
from brainvisa.maker import brainvisa_projects_versions


class Component(object):
    """BrainVISA component.

    Component is an abstract class for the component of BrainVISA installer
    repository. If the BrainVISA component is built, Component packages
    the data during the creation.

    The ifwname and ifwpackage methods must be redefined.

    Parameters
    ----------
    name : name of component.
    data : True if the component contains data, the data will be packaged
           with bv_packaging.
    configuration: Configuration object
    compress: (bool) perform compression
    """

    __metaclass__ = abc.ABCMeta
    done_components = set()
    done_created_components = set()

    @abc.abstractproperty
    def ifwname(self):
        "Return the IFW component name."
        pass

    @abc.abstractproperty
    def ifwpackage(self):
        "Return the IFWPackage of component."
        pass

    def create(self, folder):
        "Create the component in folder."
        path = "%s/%s" % (folder, self.ifwname)
        if path in Component.done_created_components \
                or (self.configuration
                    and self.configuration.is_package_excluded(self.name)):
            return
        if not os.path.isdir(path):
            os.mkdir(path)
        elif self.configuration and self.configuration.skip_existing:
            return
        self.__package_meta(path)
        if self.data:
            self.__package_data(path)
        Component.done_created_components.add(path)

    def __init__(self, name, data=False, configuration=None, compress=False):
        self.name = name
        self.configuration = configuration
        self.description = ''
        self.project = None
        self.type = None
        self.version = None
        self.licenses = None
        self.virtual = 'true'
        self.displayname = None
        self.date = None
        self.script = None
        self.data = data
        self.compress = compress
        self.default = None
        
        new_component = self.name not in Component.done_components
        if new_component:
            self.done_components.add(self.name)
        self.__init_date()
        self.__init_infos()
        if self.configuration is not None:
            self.__init_config()
            
        if new_component:
            logging.getLogger().debug("[ BVI ] Component: %s (version: %s)" \
                % (self.name, str(self.version) \
                   if not self.version is None else "unknown"))

    def __init_infos(self):
        "Initialize the component information."
        if self.name in packages_info:
            infos = packages_info[self.name]
            self.project = infos['project']
            self.type = infos['type']
            self.version = infos['version']
            if 'licences' in infos:
                self.licenses = infos['licences']
            default = infos.get( 'default_install', None )
            if default:
                self.default = 'true'
        else:
            if self.name not in self.done_components:
                logging.getLogger().warning(
                    "[ BVI ]: WARNING no information for %s" % self.name)
            self.project = ''
            self.type = 'thirdparty'
            self.version = '1.0'
        if self.type == 'test':
            self.virtual = 'false'

    def __init_config(self):
        "Initialize from the configuration file."
        conf =  self.configuration
        ex_version         = conf.exception_info_by_name(self.name, 'VERSION')
        ex_description     = conf.exception_info_by_name(self.name, 'DESCRIPTION')
        ex_displayname     = conf.exception_info_by_name(self.name, 'DISPLAYNAME')
        ex_virtual         = conf.exception_info_by_name(self.name, 'VIRTUAL')
        ex_default         = conf.exception_info_by_name(self.name, 'DEFAULT')
        msg = "[ BVI ] Package: %s => exception for %s: %s"
        if ex_virtual is not None:
            self.virtual = ex_virtual
            if self.name not in self.done_components:
                logging.getLogger().info( msg % (self.name, 'Virtual',
                                                 ex_virtual) )
        elif brainvisa_projects_versions.is_private_component(self.name):
            # private components are not virtual since they are normally
            # terminal components, individually installable.
            self.virtual = 'false'

        if self.virtual != 'true' and ex_default is not None:
            self.default = ex_default
            if self.name not in self.done_components:
                logging.getLogger().info( msg % (self.name, 'Default',
                                                 ex_default) )
        if ex_description is not None:
            self.description = ex_description
            if self.name not in self.done_components:
                logging.getLogger().info( msg % (self.name, 'Description',
                                                 ex_description) )
        if ex_displayname is not None:
            self.displayname = ex_displayname
            if self.name not in self.done_components:
                logging.getLogger().info( msg % (self.name, 'DisplayName',
                                                 ex_displayname) )
        if ex_version is not None:
            self.version = ex_version
            if self.name not in self.done_components:
                logging.getLogger().info( msg % (self.name, 'Version',
                                                 ex_version) )

    def __init_date(self):
        "Initialize the date."
        now = datetime.datetime.now()
        self.date = now.strftime("%Y-%m-%d")

    def __package_meta(self, folder):
        "Create the meta folder of IFW component."
        meta_folder = "%s/meta" % folder
        if not os.path.exists(meta_folder):
            os.mkdir(meta_folder)
        self.__copy_script(meta_folder)
        self.ifwpackage.save("%s/package.xml" % meta_folder)

    def __package_data(self, folder):
        "Create the data folder of IFW component."
        if self.configuration is not None:
            if self.configuration.is_packaging_excluded(self.name) \
                    or self.configuration.skip_repos:
                return
        data_folder = "%s/data" % folder
        if not os.path.exists(data_folder):
            os.mkdir(data_folder)
        self.__bv_packaging(data_folder)

        if not self.compress:
            return

        content_data = glob.glob("%s/*" % data_folder)
        for content in content_data:
            if not os.path.exists(content):
                continue
            if os.path.islink(content):
                continue
            archivegen(content)
            if os.path.isdir(content):
                shutil.rmtree(content)
            else:
                os.remove(content)

    def __bv_packaging(self, folder_data):
        "Use bv_packaging to package the component data."
        bv_packaging(self.name, self.type, folder_data, 
                     make_options = self.configuration.make_options,
                     platform_target = self.configuration.platform_target)
        readme = "%s/README" % folder_data
        if os.path.isfile(readme):
            os.remove(readme)

    def __clean_data(self, folder_data):
        "Replace the non compress data by the 7zip archive"
        shutil.rmtree(folder_data)
        os.mkdir(folder_data)
        file_src = "%s.7z" % (folder_data)
        file_des = "%s/%s.7z" % (folder_data, self.name.replace('-', '_'))
        shutil.move(file_src, file_des)

    def __copy_script(self, folder):
        "Copy the script in meta folder. Warning: must be call before \
        self.ifwpackage."
        if self.configuration is None:
            return

        value_script = self.configuration.script_by_name(self.name)
        if value_script is None:
            return
        self.script = 'script.qs'
        src = "%s/%s" % (Paths.BVI_SHARE_SCRIPTS, value_script)
        dst = "%s/script.qs" % folder
        shutil.copyfile(src, dst)
