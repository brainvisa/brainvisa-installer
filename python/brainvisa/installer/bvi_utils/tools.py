#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Procedures to simplify the use of external tools.
#

from __future__ import print_function

import os
import sys
import subprocess
import logging
import hashlib
import distutils.spawn

from brainvisa.installer.bvi_utils.system import System
from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_utils.bvi_exception import BVIException


def ifw_version(binary_creator_command=None, platform=None):
    """Try to guess IFW version.
    As the commands do not provide this info, all we can do for now is to try
    to find the "devtool" command, and guess it is version 2 if it is found,
    and 1 otherwise.
    """
    if not platform:
        platform = System.platform()

    if not binary_creator_command:
        bc = distutils.spawn.find_executable(
            Paths.binary_name(Paths.IFW_BINARYCREATOR, platform))
    else:
        bc = binary_creator_command

    if not bc:
        return []  # undefined
    real_bc = os.path.realpath(bc)
    path = os.path.dirname(real_bc)
    if os.path.exists(
        os.path.join(path,
                     Paths.binary_name(Paths.IFW_DEVTOOL, platform))):
        return [2, ]
    return [1, ]


class PathTranslationType:
    HOST_TO_TARGET = 0
    TARGET_TO_HOST = 1


def translate_path_wine(path,
                        translation_type=PathTranslationType.HOST_TO_TARGET):
    # print('==== translate_path_wine')
    wp = distutils.spawn.find_executable(Paths.WINEPATH)
    if translation_type == PathTranslationType.HOST_TO_TARGET:
        cmd = [wp, '-w', path]

    elif translation_type == PathTranslationType.TARGET_TO_HOST:
        cmd = [wp, '-u', path]

    else:
        raise TypeError('Wrong PathTranslationType %d' % translation_type)

    return subprocess.check_output(cmd, universal_newlines=True).strip()


def translate_path(path, platform_target,
                   translation_type=PathTranslationType.HOST_TO_TARGET):
    """Translate path between platform host and target."""
    platform_host = System.platform()
    platform_host_family = System.platform_family(platform_host)
    platform_target_family = System.platform_family(platform_target)

    # print('==== translate_path')
    if platform_host != platform_target.upper():
        if platform_host_family == System.Family.Linux \
                and platform_target_family == System.Family.Win:
            return translate_path_wine(path, translation_type)
        else:
            raise RuntimeError('No known path translation method between '
                               '%s (%s family) and %s (%s family) systems'
                               % (platform_host, platform_host_family,
                                  platform_target, platform_target_family))

    else:
        return path


def binarycreator(
    installer_path, repository_path, additional_repositories=[],
    online_only=False, offline_only=False, exclude=None, include=None,
        platform_target=System.platform(), command=None):
    """The binarycreator tool creates an IFW installer.

    Parameters
    ----------
    installer_path          : full path of installer binary.
    repository_path         : full path of temporary repository.
    additional_repositories : additional repositories to find packages in.
    online_only             : True if the installer is only online
                              (default False).
    offline_only            : True if the installer is only offline
                              (default False).
    exclude                 : list of excluded package's names (default None).
    include                 : list of included package's names (default None).
    platform_target         : target platform to generate installer binary on
                              (default is the host platform)
    command                 : binarycreator command to use (default:)
    """

    param_online_only = ['--online-only'] if online_only else []
    param_offline_only = ['--offline-only'] if offline_only else []
    param_exclude = ['--exclude', exclude.join(',')] if exclude else []
    param_include = ['--include', include.join('')] if include else []
    param_config = [
        '-c', translate_path('%s/config/config.xml' % repository_path,
                             platform_target)]
    param_packages = ['-p', translate_path('%s/packages' % repository_path,
                                           platform_target)]
    for r in additional_repositories:
        param_packages += ['-p', translate_path(r, platform_target)]

    path = os.path.dirname(installer_path)
    if not os.path.exists(path):
        os.makedirs(path)

    # Starts binary creator through target bv_env
    cmd = [command if command else Paths.binary_name(Paths.IFW_BINARYCREATOR,
                                                     platform_target)] \
        + param_online_only + param_offline_only + param_exclude \
        + param_include + param_config + param_packages \
        + [translate_path(installer_path, platform_target)]
    print(' '.join(cmd))
    subprocess.check_call(cmd)

    if System.platform() == System.MacOSX:
        return  # don't do the .md5 now: we must build the .dmg first.
    # build the MD5 sum file
    m = hashlib.md5()
    m.update(open(installer_path, 'rb').read())
    mdsum = m.digest()
    if sys.version_info[0] >= 3:
        mdsum_str = ''.join(['%02x' % x for x in mdsum])
    else:
        mdsum_str = ''.join(['%02x' % ord(x) for x in mdsum])
    open(installer_path + '.md5', 'w').write(mdsum_str)


def repogen(path_repository_in, path_repository_out,
            components=None, update=False,
            exclude=None):  # pylint: disable=R0913
    """The repogen tool generates an online IFW repositoriy.

    Parameters
    ----------
    path_repository_in  : full path of temporary repository.
    path_repository_out : full path of IFW repository.
    components          : additional components (default None).
    update              : True if the existing IFW repository must be updated.
    exclude             : list of excluded package's names (default None).
    """
    param_components = [components.join(',')] if exclude else []
    param_update = ['--update'] if update else []
    param_exclude = ['--exclude', exclude.join(',')] if exclude else []
    # param_updateurl = '-u %s' % updateurl  if updateurl else ''
    param_packages = ["-p", "%s/packages" % path_repository_in]

    cmd = [Paths.binary_name(Paths.IFW_REPOGEN, System.platform())] \
        + param_packages + param_update + param_exclude \
        + param_components + [path_repository_out]
    # param_updateurl,
    print(' '.join(cmd))
    subprocess.check_call(cmd)


def archivegen(folder):
    """The archivegen tool compresses the files in folder as a 7zip archive.

    The archive will have the same name what the folder with the 7z extension.

    Parameter
    ---------
    folder:
        folder with data which must be compressed.
    """
    command = Paths.binary_name(Paths.IFW_ARCHIVEGEN, System.platform())
    archive = '%s.7z' % folder

    args = [command] + Paths.ARCHIVEGEN_OPTIONS + [archive, '%s' % folder]
    print(' '.join(args))
    if os.path.exists(archive):
        os.unlink(archive)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=folder)
    result = process.wait()
    logging.getLogger().info(result)
    if result < 0:
        raise BVIException(BVIException.ARCHIVEGEN_FAILED, folder)


def bv_packaging(name, type_, folder, make_options=None, platform_target=None):
    """Package a component with no dependency.

    Parameters
    ----------
    name   : package name.
    type_  : type of package: run, doc, usrdoc, devdoc, test.
    folder : destination full path.
    platform_target : target platform to generate packages for
    """
    args = [os.path.join(Paths.BV_BIN,
                         Paths.binary_name(Paths.BV_ENV_HOST,
                                           System.platform())),
            Paths.binary_name('python', System.platform()),
            os.path.join(Paths.BV_BIN, Paths.BV_PACKAGING),
            'dir',
            '-o', folder,
            '--wrappers',
            '--no-deps',
            '--installer']

    if make_options is not None and len(make_options.strip()) > 0:
        args += ['--make-options', make_options]

    if platform_target is not None and len(platform_target.strip()) > 0:
        args += ['--platform-target', platform_target]

    args += ['+name=%s,type=%s' % (name, type_)]
    subprocess.check_call(args)
