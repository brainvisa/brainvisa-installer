#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = "Hakim Taklanti"
__copyright__   = "Copyright 2013-2015, CEA / Saclay"
__credits__     = ["Hakim Taklanti",
                   "Yann Cointepas",
                   "Denis Rivière",
                   "Nicolas Souedet"]
__license__     = "CeCILL V2"
__version__     = "1.0"
__maintainer__  = "Hakim Taklanti"
__email__       = "hakim.taklanti@altran.com"
__status__      = "release"


#  This software and supporting documentation are distributed by
#      Institut Federatif de Recherche 49
#      CEA/NeuroSpin, Batiment 145,
#      91191 Gif-sur-Yvette cedex
#      France
#
# This software is governed by the CeCILL-B license under
# French law and abiding by the rules of distribution of free software.
# You can  use, modify and/or redistribute the software under the 
# terms of the CeCILL-B license as circulated by CEA, CNRS
# and INRIA at the following URL "http://www.cecill.info". 
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or 
# data to be ensured and,  more generally, to use and operate it in the 
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.

import os.path
import argparse
import logging
import shutil
import re
import subprocess
from logging.handlers import RotatingFileHandler

from brainvisa.installer.project import Project
from brainvisa.installer.package import Package
from brainvisa.installer.repository import Repository
from brainvisa.installer.bvi_xml.configuration import Configuration
from brainvisa.installer.bvi_utils.tools import repogen, binarycreator
from brainvisa.installer.bvi_utils.system import System

from brainvisa.maker.brainvisa_projects import ordered_projects
from brainvisa.compilation_info import packages_info
from brainvisa.compilation_info import packages_dependencies
import brainvisa.maker.brainvisa_projects_versions as projects_versions


#-----------------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------------

MESSAGE_HELP_HEADER = """BrainVISA Installer Help
BrainVISA Build Installer allows to build:
  - an offline installer binary that contains all specified BrainVISA packages and the dependencies;
  - an online installer binary;
  - a repository for the online installer.
"""

MESSAGE_HELP_EPILOG = """
Example:
> ./bv_build_installer.py -p soma aims anatomist axon -i $HOME/brainvisa/installer -r $HOME/brainvisa/repository --online-only
"""

INFO_TABLE_ROW = """<tr>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
</tr>
"""

MESSAGE_INVALID_PROJECT = "[ BVI ] Error: The project %s does not exist!."
MESSAGE_INVALID_NAME = "[ BVI ] Error: The component %s does not exist!."
MESSAGE_INVALID_CONFIG = "[ BVI ] Error: The file %s does not exist!."
MESSAGE_INVALID_RELEASE = "[ BVI ] Error: The release number %s does not match the required pattern (numbers separated by dots)."

MESSAGE_BVI_HEADER = """
===============================================================
=================== [ BrainVISA Installer ] ===================
===============================================================
"""

MESSAGE_BVI_CONFIGURATION = """
===============================================================
========= [ BVI ]: Create configuration repository... =========
===============================================================
"""

MESSAGE_BVI_INFORMATION = """
===============================================================
============ [ BVI ]: Generate packages infos... ==============
===============================================================
"""

MESSAGE_BVI_REPOSITORY = """
===============================================================
============== [ BVI ]: Create final repository... ============
===============================================================
"""

MESSAGE_BVI_INSTALLER = """
===============================================================
============== [ BVI ]: Create installer binary... ============
===============================================================
"""

HTML_HEADER = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <meta content="Hakim Taklanti" name="author" />
        <meta content="2013-10-14T17:24:52+0200" name="date" />
        <meta content="CEA / Saclay" name="copyright" />
        <meta content="BrainVISA; Neurospin; CEA; Saclay; MIRCEN" name="keywords" />
        <meta content="" name="description" />
        <meta content="NOINDEX, NOFOLLOW" name="ROBOTS" />
        <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
        <meta content="application/xhtml+xml; charset=UTF-8" http-equiv="content-type" />
        <meta content="text/css" http-equiv="content-style-type" />
        <meta content="0" http-equiv="expires" />
        <title>BrainVISA Packages</title>
        <style type="text/css">
            table {
                border:1px solid black;
                text-align: center;
            }

            td, th {
                border:1px solid black;
                padding:8px;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>BrainVISA Packages</h1>
        </header>
        <section>
            <article>
                <table>
                   <caption>Packages List</caption>
                   <thead>
                       <tr>
                            <th>Project</th>
                            <th>Package</th>
                            <th>Type</th>
                            <th>Version</th>
                            <th>License</th>
                       </tr>
                   </thead>
                   <tbody>
"""

HTML_FOOTER = """
                    </tbody>
                </table>
            </article>
        </section>
    
        <footer>
            <p style="text-align:center;">Copyright CEA - Tous droits réservés<br />
            <a style="text-align:center;" href="http://brainvisa.info">BrainVISA.info</a></p>
        </footer>
    </body>
</html>
"""


#-----------------------------------------------------------------------------
# Applications
#-----------------------------------------------------------------------------

class Application(object):
    "Entry point of BrainVISA Installer."

    def start(self):
        "Start BrainVISA Installer process."
        logging.getLogger().info(MESSAGE_BVI_HEADER)
        #self.__configure_logging()
        self.__create_configuration()
        self.__create_information()
        self.__create_repository()
        self.__create_installer()
        self.__create_hacks()
        logging.getLogger().info("End.\n")

    def __init__(self, argv):
        "Parse the command line arguments."
        parser = argparse.ArgumentParser(
            formatter_class = argparse.RawDescriptionHelpFormatter,
            description     = MESSAGE_HELP_HEADER,
            epilog          = MESSAGE_HELP_EPILOG)

        parser.add_argument('-p', '--projects',
            type    = valid_projects,
            nargs   = '+',
            metavar = 'project',
            help    = 'Projects to include in the installer and the repository')

        parser.add_argument('-n', '--names',
            type    = valid_names,
            nargs   = '+',
            metavar = 'name',
            help    = 'Package names to include in the installer and the repository')

        parser.add_argument('-t', '--types',
            nargs   = '+',
            choices = ['run', 'dev', 'usrdoc', 'devdoc', 'test'],
            default = ['run', 'dev', 'usrdoc', 'devdoc', 'test'],
            metavar = 'types',
            help    = 'Package\'s types (default: "run", "dev", "usrdoc", "devdoc" and "test")')

        parser.add_argument('--online-only',
            action  = 'store_true',
            help    = 'Create only an online installer')

        parser.add_argument('--offline-only',
            action  = 'store_true',
            help    = 'Create only an offline installer')

        parser.add_argument('--repository-only',
            action  = 'store_true',
            help    = 'Create only the repository for the online installer')

        parser.add_argument('--compress',
            action  = 'store_true',
            help    = 'The packages data in the temporary repository will be compressed [experimental].')

        parser.add_argument('-i', '--installer',
            default = 'BrainVISA_Suite-Installer',
            metavar = 'file',
            help    = 'Installer name (optional only if --repository-only is specified).')

        parser.add_argument('-r', '--repository',
            default = None,
            metavar = 'dir',
            required= True,
            help    = 'Repository name.')

        parser.add_argument('-c', '--config',
            type    = valid_config,
            default = None,
            metavar = 'file',
            help    = 'Additional configuration XML file')

        parser.add_argument('--no-main-config',
            action  = 'store_true',
            help    = 'don\'t read the main BrainVisa config file. Must be used with the -c option')

        parser.add_argument('--qt_menu_nib',
            default = None,
            help    = 'For Mac OS X 10.5: copy the specified qt_menu.nib folder in the \
            installer OSX App package. Use this option, if the OS X installer did not \
            find the qt_menu.nib folder.')

        parser.add_argument('--release',
            type    = valid_release,
            default = None,
            help    = 'force repository release version. default: use BrainVISA release version from the current build.')

        parser.add_argument('--i2bm',
            action  = 'store_true',
            help    = 'Include I2BM private components - by default such private components are excluded from the package.')

        parser.add_argument('--data',
            action  = 'store_true',
            help    = 'Package only data packages (which are excluded from '
            'normal packaging).')

        parser.add_argument('-v', '--version',
            action  = 'version',
            version = '%(prog)s [' + __status__ + '] - ' + __version__,
            help    = 'Show the version number.')

        parser.add_argument('--no-thirdparty',
            action  = 'store_true',
            help    = 'Do not package thirdparty libraries, and ignore them in dependencies.')

        parser.add_argument('--no-dependencies',
            action  = 'store_true',
            help    = 'Do not package dependencies: take only explicitely named packages/projects. Their dependencies will still be marked so they must either already exist in the repository, either exist in another repository.')

        parser.add_argument('--platform-target',
            dest = 'platform_target',
            default = None,
            help    = 'target platform to use for cross compilation (default: %s)' % System.platform().lower())

        parser.add_argument('--platform_name',
            default = None,
            help    = 'force platform name in packages repository URL (default: %s)' % System.platform().lower())

        parser.add_argument('--make-options',
            dest = 'make_options',
            default = None,
            help    = 'make options to use during components packaging')
        
        parser.add_argument('--binary-creator-cmd', dest='binary_creator_command',
            default = None,
            help='Path to the binary creator command to use to generate'
            'the installer.')
        
        parser.add_argument('--skip-repos', dest='skip_repos',
            action='store_true',
            help='Skip initial (temp) repository creation. Assumes it has already been done.')

        parser.add_argument('--skip-repogen', dest='skip_repogen',
            action='store_true',
            help='Skip repogen (final repository creation + compression). Assumes it has already been done.')

        parser.add_argument('--skip-existing', dest='skip_existing',
            action='store_true',
            help='Don\'t rebuild components which already have a directory in '
            'the temporary repository directory.')

        self.__configure_logging()
        args = parser.parse_args(argv[1:])

        if args.online_only + args.offline_only + args.repository_only > 1:
            logging.getLogger().error("[ BVI ] Error: --online-only, --offline-only and \
            --repository-only are incompatible.")
            exit(1)

        if args.qt_menu_nib is not None:
            if args.installer is None:
                logging.getLogger().error("[ BVI ] Error: --installer must be specified if \
                --qt_menu_nib is used.")
                exit(1)
            if System.platform() != System.MacOSX:
                logging.getLogger().error("[ BVI ] Error: --qt_menu_nib is only for Mac OS X.")
                exit(1)

        self.args = args
        self.logging_level = logging.DEBUG
        if self.args.no_main_config:
            kwargs = { 'filename': self.args.config }
        else:
            kwargs = { 'alt_filename' : self.args.config }
        if self.args.release is not None:
            kwargs[ 'release' ] = self.args.release
        if self.args.no_thirdparty:
            kwargs['with_thirdparty'] = False
        if self.args.no_dependencies:
            kwargs['with_dependencies'] = False
        if self.args.platform_target:
            kwargs['platform_target'] = self.args.platform_target
            if not self.args.platform_name:
                # Defaultly use target platform as platform name
                self.args.platform_name = self.args.platform_target
        if self.args.platform_name:
            kwargs['platform_name'] = self.args.platform_name
          
        kwargs['make_options'] = self.args.make_options
        kwargs['binary_creator_command'] = self.args.binary_creator_command
        kwargs['skip_repos'] = self.args.skip_repos
        kwargs['skip_repogen'] = self.args.skip_repogen
        kwargs['skip_existing'] = self.args.skip_existing
        kwargs['data_packages'] = self.args.data
        kwargs['private_repos'] = self.args.i2bm
        self.config = Configuration(**kwargs)
        self.components = self.__group_components()

    def __configure_logging(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
        file_handler = RotatingFileHandler('bv_build_installer.log', 'a', 1000000, 1)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(logging.DEBUG)
        logger.addHandler(steam_handler)

    def __group_components(self):
        "Group the projets and packages in one list. The projects and the \
        packages have the same interface."
        res = list()
        if self.args.projects:
            for project in self.args.projects:
                res.append(Project(project, self.config, self.args.types,
                    compress = self.args.compress,
                    remove_private=not self.args.i2bm))
        if self.args.names:
            for name in self.args.names:
                cls = Package.package_factory(name, self.config)
                res.append(cls(name, self.config,
                               compress = self.args.compress))
        return res

    def __create_configuration(self):
        "Create the temporary repository for the configuration."
        logging.getLogger().info(MESSAGE_BVI_CONFIGURATION)
        temporary_folder = "%s_tmp" % self.args.repository
        rep = Repository(temporary_folder, self.config, self.components,
            with_dependencies=not self.args.no_dependencies, 
            with_thirdparty=not self.args.no_thirdparty)
        rep.create()

    def __create_information(self):
        "Create the packages information file."
        logging.getLogger().info(MESSAGE_BVI_INFORMATION)
        info_file = "%s_infos.html" % self.args.repository
        write_info(info_file, self.args.projects, self.args.names,
            remove_private=not self.args.i2bm,
            with_dependencies=not self.args.no_dependencies,
            with_thirdparty=not self.args.no_thirdparty)

    def __create_repository(self):
        "Create the online repository."
        if not self.args.offline_only and not self.args.skip_repogen:
            logging.getLogger().info(MESSAGE_BVI_REPOSITORY)
            repogen("%s_tmp" % self.args.repository, self.args.repository, 
                    update=True)

    def __create_installer(self):
        "Create the binary installer."
        if not self.args.repository_only:
            logging.getLogger().info(MESSAGE_BVI_INSTALLER)
            binarycreator(self.args.installer, "%s_tmp" % self.args.repository,
                online_only = self.args.online_only,
                offline_only = self.args.offline_only,
                platform_target = self.args.platform_target \
                                  if self.args.platform_target \
                                  else System.platform().lower(),
                command = self.args.binary_creator_command \
                          if self.args.binary_creator_command \
                          else None)

    def __create_hacks(self):
        "Regroup all hacks for specific problems."
        qt_menu_nib = None
        if System.platform() == System.MacOSX \
                and self.args.qt_menu_nib is None:
            # try to find qt_menu.nib in QtIFW
            import distutils.spawn
            binarycreator = distutils.spawn.find_executable(
                Paths.IFW_BINARYCREATOR)
            if binarycreator:
                real_path = os.path.realpath(binarycreator)
                path = os.path.dirname(os.path.dirname(real_path))
                qt_menu_nib = os.path.join(
                    path, "Uninstaller.app/Contents/Resources/qt_menu.nib")
                if not os.path.isdir(qt_menu_nib):
                    qt_menu_nib = None  # doesn't work
        else:
            qt_menu_nib = self.args.qt_menu_nib
        if not qt_menu_nib is None:
            src = qt_menu_nib
            dst = "%s.app/Contents/Resources/qt_menu.nib" % self.args.installer
            try:
                shutil.copytree(src, dst)
            except:
                # copying file attributes on the network may fail,
                # but copy is OK.
                pass

        if System.platform() == System.MacOSX \
                and not self.args.repository_only:
            # create .dmg
            import distutils.spawn
            create_dmg = distutils.spawn.find_executable('create-dmg')
            if create_dmg:
                installer_path = '%s.dmg' % self.args.installer
                cmd = [create_dmg, '--volname', 'BrainVISA-installer',
                      '--volicon',
                      '%s_tmp/config/icon.png' % self.args.repository,
                      installer_path, '%s.app' % self.args.installer]
                subprocess.check_call(cmd)
            # build the MD5 sum file
            import hashlib
            m = hashlib.md5()
            m.update(open(installer_path, 'rb').read())
            mdsum = m.digest()
            mdsum_str = ''.join(['%02x' % ord(x) for x in mdsum])
            open(installer_path + '.md5', 'w').write(mdsum_str)


#-----------------------------------------------------------------------------
# Methods
#-----------------------------------------------------------------------------
def valid_projects(arg):
    "Check if the project exists."
    if not arg in ordered_projects and arg not in packages_info:
        error = MESSAGE_INVALID_PROJECT % arg
        logging.getLogger().error(error)
        raise argparse.ArgumentTypeError(error)
    return arg


def valid_names(arg):
    "Check if the component exists."
    if not arg in packages_info:
        error = MESSAGE_INVALID_NAME % arg
        logging.getLogger().error(error)
        raise argparse.ArgumentTypeError(error)
    return arg


def valid_config(arg):
    "Check if the config file exist."
    if not os.path.isfile(arg):
        error = MESSAGE_INVALID_CONFIG % arg
        logging.getLogger().error(error)
        raise argparse.ArgumentTypeError(error)
    return arg


def valid_release(arg):
    "Check if the release version is a valid version number (x.y.z)."
    if not re.match('^[0-9]+(\.[0-9]+)*$', arg):
        error = MESSAGE_INVALID_RELEASE % arg
        logging.getLogger().error(error)
        raise argparse.ArgumentTypeError(error)
    return arg


def write_info(filename, projects, names, remove_private, 
        with_dependencies=True, with_thirdparty=True):
    "Write a HTML table with the list of packages."
    list_packages = set()
    with open(filename, 'w') as fo:
        fo.write(HTML_HEADER)
        if projects:
            for project in projects:
                for component in \
                        projects_versions.project_components(
                            project,remove_private=remove_private  ):
                    write_info_package(fo, component, list_packages,
                        with_dependencies, with_thirdparty)
        if names:
            for name in names:
                write_info_package(fo, name, list_packages, with_dependencies,
                    with_thirdparty)
        fo.write(HTML_FOOTER)


def write_info_package(fo, component, list_packages, with_dependencies=True,
        with_thirdparty=True):
    "Write a HTML row with the package's information."
    info_package     = component
    info_project     = ''
    info_type         = ''
    info_version     = ''
    info_licenses     = ''
    infos = packages_info.get(component)
    if infos:
        info_type = infos.get('type', '')
        info_version = infos.get('version', '')
        info_licenses = infos.get('licences', '')
        info_project = infos.get('project', '')
        info_licenses = ', '.join(info_licenses)

    html = INFO_TABLE_ROW % (info_project, info_package, info_type,
        info_version, info_licenses)
    if not info_package in list_packages and \
            (with_thirdparty or info_type != 'thirdparty'):
        fo.write(html)
        list_packages.add(info_package)

    if with_dependencies:
        dependencies = packages_dependencies.get(info_package)
        if dependencies:
            for dependency in dependencies:
                write_info_package(fo, dependency[1], list_packages,
                    with_dependencies, with_thirdparty)

#-----------------------------------------------------------------------------
# Main
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    app = Application(sys.argv)
    app.start()
