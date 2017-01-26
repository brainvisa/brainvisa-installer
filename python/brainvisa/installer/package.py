#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import brainvisa.installer.bvi_utils.format as ft
from brainvisa.installer.component import Component
from brainvisa.installer.bvi_xml.ifw_package import IFWPackage
from brainvisa.installer.bvi_xml.tag_dependency import TagDependency
from brainvisa.compilation_info import packages_dependencies, packages_info


class Package(Component):
    """BrainVISA package."""

    @property
    def ifwname(self):
        p_name = ft.ifw_name(self.project)
        c_name = ft.ifw_name(self.name)
        res = {
            'run'       : "brainvisa.app.%s.run.%s" % (p_name, c_name),
            'usrdoc'    : "brainvisa.app.%s.usrdoc.%s" % (p_name, c_name),
            'dev'       : "brainvisa.dev.%s.dev.%s" % (p_name, c_name),
            'devdoc'    : "brainvisa.dev.%s.devdoc.%s" % (p_name, c_name),
            'test'      : "brainvisa.test.%s.test.%s" % (p_name, c_name),
            'thirdparty': "brainvisa.app.thirdparty.%s" % (c_name)
        }
        return res[self.type]

    @property
    def ifwpackage(self):
        tag_deps = list()
        if self.dependencies:
            for dep_pack in self.dependencies:
                tag_dep = TagDependency(
                    name=dep_pack.ifwname, 
                    version=self.make_valid_version(dep_pack.version))
                tag_deps.append(tag_dep)
        if self.type == 'run':
            tag_deps.append(TagDependency(
                name="brainvisa.app.thirdparty.bv_env"))
        if self.licenses:
            for lic in self.licenses:
                valid_name = ft.ifw_name(lic)
                license_component = "brainvisa.app.licenses.%s" % valid_name
                tag_dep = TagDependency(name=license_component)
                tag_deps.append(tag_dep)

        package = IFWPackage(
            DisplayName     = self.displayname, 
            Description     = self.description, 
            Version         = self.make_valid_version(self.version),
            ReleaseDate     = self.date, 
            Name            = self.ifwname, 
            TagDependencies = tag_deps, 
            Virtual         = self.virtual,
            Script          = self.script,
            TagLicenses     = None,
            Default         = self.default)
        return package

    def create(self, folder):
        if not self.write_it:
            logging.getLogger().info(
                "[ BVI ] PACKAGE: %s => skipping writing" % self.name)
            return
        super(Package, self).create(folder)
        if self.dependencies is None:
            return
        for dep_pack in self.dependencies:
            dep_pack.create(folder)

    def __init__(self, name, configuration=None, compress=False,
            write_it=True):
        super(Package, self).__init__(name, True, configuration, compress)
        self.dependencies = None
        self.write_it = write_it
        if self.displayname is None:
            self.displayname = self.name.title()
        self.__init_dependencies()

    def __init_dependencies(self):
        if not self.name in packages_dependencies:
            return
        infos_deps = list(packages_dependencies[self.name])
        if len(infos_deps) > 0:
            self.dependencies = list()
        for info in infos_deps:
            dep_name = info[1].decode('utf-8')
            pinfo = packages_info[dep_name]
            if not self.configuration.with_thirdparty \
                    and pinfo['type'] == 'thirdparty':
                continue
            dep_pack = Package(dep_name, self.configuration,
                write_it=self.configuration.with_dependencies)
            self.dependencies.append(dep_pack)

    @staticmethod
    def package_factory(name, config):
        ex_pack_class = config.exception_info_by_name(name, 'PACKAGING_CLASS')
        if ex_pack_class is not None:
            modcls = ex_pack_class.split('.')
            if len(modcls) > 1:
                modname = '.'.join(modcls[:-1])
                import importlib
                mod = importlib.import_module(modname)
                cls = getattr(mod, modcls[-1])
            else:
                cls = globals().get(modcls)
            return cls
        return Package

    @staticmethod
    def make_valid_version(version):
        vversion = [c for c in version if c in '.0123456789']
        return ''.join(vversion)
