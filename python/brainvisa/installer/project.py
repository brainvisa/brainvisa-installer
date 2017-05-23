#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import os.path
import collections
import logging
import shutil

from brainvisa.installer.package import Package
from brainvisa.installer.component import Component
import brainvisa.installer.bvi_utils.format as ft
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage
from brainvisa.installer.bvi_xml.tag_dependency import TagDependency
from brainvisa.installer.bvi_utils.bvi_exception import BVIException

from brainvisa.compilation_info import packages_info
from brainvisa.maker.brainvisa_projects import ordered_projects
from brainvisa.maker.brainvisa_projects_versions import project_version
from brainvisa.maker.brainvisa_projects_versions import project_description
from brainvisa.maker.brainvisa_projects_versions import project_components
from brainvisa.maker.brainvisa_projects_versions import is_default_project

class Project(Component):
    """BrainVISA project.

    A project contains a set of packages.

    Parameters
    ----------
    name             : BrainVISA project name. It must be in brainvisa_projects module.
    configuration    : Configuration object, using to configure the subcategory for each
                      project (see CATEGORY section).
    types            : list of type's names: run, usrdoc, dev, devdoc, test.
                      Default: ['run', 'usrdoc', 'dev', 'devdoc', 'test']
    compress         : (bool, optional) perform compression
    remove_private   : (bool, optional) remove private components in the project
    """

    @property
    def ifwname(self):
        p_name = ft.ifw_name(self.name)
        res = {
            'run'       : "brainvisa.app.%s" % (p_name),
            'usrdoc'    : "brainvisa.app.%s" % (p_name),
            'dev'       : "brainvisa.dev.%s" % (p_name),
            'devdoc'    : "brainvisa.dev.%s" % (p_name),
            'test'      : "brainvisa.test.%s" % (p_name)
        }
        return res[self.type]

    @property
    def ifwpackage(self):
        package = IFWPackage(
            DisplayName     = self.name.title(),
            Description     = self.description,
            Version         = self.version,
            ReleaseDate     = self.date,
            Name            = self.ifwname,
            Script          = self.script,
            Virtual         = 'false')
        return package

    def create(self, folder):
        self.__create_packages(folder)
        for type_ in self.types:
            self.type = type_
            self.__create_subcategory(folder)
            super(Project, self).create(folder)

    def __init__(self, name, configuration, types = None, compress=False,
            remove_private=False): #pylint: disable=W0231
        super(Project, self).__init__(name)
        logging.getLogger().info( "[ BVI ] PROJECT: %s" % name )
        types = types or ['run', 'usrdoc', 'dev', 'devdoc', 'test']
        if not name in ordered_projects and not name in packages_info:
            raise BVIException(BVIException.PROJECT_NONEXISTENT, name)
        super(Project, self)._Component__init_date()
        self.name = name
        self.project = name
        self.types = types
        self.type = None
        self.compress = compress
        self.configuration = configuration
        self.licenses = None
        self.data = None
        self.script = None
        self.remove_private = remove_private
        self.version = project_version(self.name)
        self.description = project_description(self.name)
        self.dep_packages = collections.defaultdict(list)
        first_component = project_components(self.name, self.remove_private)[0]
        ex_version = self.configuration.exception_info_by_name(first_component, 'VERSION')
        if ex_version is None:
            if first_component in packages_info:
                self.version = packages_info[first_component]['version']
        else:
            self.version = ex_version

    def __create_subcategory(self, folder):
        cat = self.configuration.category_by_id(self.type)
        name = "%s.%s" % (self.ifwname, self.type)
        folder_package = "%s/%s" % (folder, name)
        if not os.path.isdir(folder_package):
            os.mkdir(folder_package)
        meta_folder = "%s/meta" % folder_package
        if os.path.isdir(meta_folder):
            shutil.rmtree(meta_folder)
        os.mkdir(meta_folder)
        if self.__is_default(self.type):
            is_default = 'true'
        else:
            is_default = 'false'
        p = IFWPackage( DisplayName = cat.Name,
                        Description = cat.Description,
                        Version     = self.version,
                        ReleaseDate = self.date,
                        SortingPriority = cat.Priority,
                        Name        = name,
                        Virtual     = 'false',
                        Default     = is_default,
                        TagDependencies = self.__clean_dependencies_doublons())
        p.save("%s/%s/meta/package.xml" % (folder, name))

    def __is_default(self, type):
        if is_default_project(self.name) and type in ('run', 'usrdoc'):
            return True
        cat = self.configuration.category_by_id(type)
        if cat.Default == 'true':
            return True
        return False

    def __create_packages(self, folder):
        components = project_components(self.name, self.remove_private)
        for package_name in components:
            for type_name in self.types:
                ext = '-%s' % type_name
                if type_name == 'run':
                    ext = ''
                full_name = "%s%s" % (package_name, ext)
                if full_name in packages_info:
                    if self.configuration.is_package_excluded(full_name):
                        continue
                    cls = Package.package_factory(full_name,
                                                  self.configuration)
                    pack = cls(full_name, self.configuration,
                               compress=self.compress)
                    pack.create(folder)
                    if not self.__is_in_dependencies(pack, type_name):
                        self.dep_packages[type_name].append(pack)

    def __is_in_dependencies(self, package, type_name):
        for dep in self.dep_packages[type_name]:
            if dep.ifwname == package.ifwname:
                return True
        return False

    @classmethod
    def __is_in_tagdependencies(cls, tagdepency, tagdependencies):
        for tag in tagdependencies:
            if tag.text == tagdepency:
                return True
        return False

    def __clean_dependencies_doublons(self):
        clean_tagdependencies = list()
        for dep_pack in self.dep_packages[self.type]:
            tagdependency = TagDependency(
                name=dep_pack.ifwname,
                version=dep_pack.version,
                comparison='=')
            if not self.__is_in_tagdependencies(tagdependency, clean_tagdependencies):
                clean_tagdependencies.append(tagdependency)
        return clean_tagdependencies
