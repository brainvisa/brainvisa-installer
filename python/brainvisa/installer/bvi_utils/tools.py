#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Procedures to simplify the use of external tools.
#

import os
import sys
import subprocess
import logging
import md5
import distutils.spawn

from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_utils.bvi_exception import BVIException

def ifw_version():
    """Try to guess IFW version.
    As the commands do not provide this info, all we can do for now is to try
    to find the "devtool" command, and guess it is version 2 if it is found,
    and 1 otherwise.
    """
    exe = ""
    if sys.platform.startswith("win"):
        exe = ".exe"
    bc = distutils.spawn.find_executable("binarycreator" + exe)
    if not bc:
        return []  # undefined
    real_bc = os.path.realpath(bc)
    path = os.path.dirname(real_bc)
    if os.path.exists(os.path.join(path, "devtool" + exe)):
        return [2,]
    return [1,]


def binarycreator(installer_path, repository_path, online_only=False, 
    offline_only=False, exclude=None, include=None):
    """The binarycreator tool creates an IFW installer.

    Parameters
    ----------
    installer_path  : full path of installer binary.
    repository_path : full path of temporary repository.
    online_only     : True if the installer is only online (default False).
    offline_only     : True if the installer is only offline (default False).
    exclude         : list of excluded package's names (default None).
    include         : list of included package's names (default None).
    """

    param_online_only = ['--online-only'] if online_only else []
    param_offline_only = ['--offline-only'] if offline_only else []
    param_exclude = ['--exclude', exclude.join(',')] if exclude else []
    param_include = ['--include', include.join('')] if include else []
    param_config = ['-c', '%s/config/config.xml' % repository_path]
    param_packages = ['-p', '%s/packages' % repository_path]

    path = os.path.dirname(installer_path)
    if not os.path.exists(path):
        os.makedirs(path)

    cmd = [Paths.IFW_BINARYCREATOR] \
        + param_online_only + param_offline_only + param_exclude \
        + param_include + param_config + param_packages + [installer_path]
    print ' '.join(cmd)
    subprocess.check_call(cmd)

    if sys.platform == "darwin":
        return  # don't do the .md5 now: we must build the .dmg first.
    # build the MD5 sum file
    m = md5.new()
    m.update(open(installer_path, 'rb').read())
    mdsum = m.digest()
    mdsum_str = ''.join(['%02x' % ord(x) for x in mdsum])
    open(installer_path + '.md5', 'w').write(mdsum_str)


def repogen(path_repository_in, path_repository_out, 
            components = None, update=False,
            exclude=None): #pylint: disable=R0913
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
    #param_updateurl = '-u %s' % updateurl  if updateurl else ''
    param_packages = ["-p", "%s/packages" % path_repository_in]

    cmd = [Paths.IFW_REPOGEN] \
        + param_packages + param_update + param_exclude \
        + param_components + [path_repository_out]
        #param_updateurl,
    print ' '.join(cmd)
    subprocess.check_call(cmd)


def archivegen(folder):
    """The archivegen tool compresses the files in folder as a 7zip archive.

    The archive will have the same name what the folder with the 7z extension.

    Parameter
    ---------
    folder - folder with data which must be compressed.
    """
    args = ['archivegen', '%s.7z' % folder, '%s' % folder]
    print ' '.join(args)
    process = subprocess.Popen(args, stdout=subprocess.PIPE, cwd=folder)
    result = process.wait()
    logging.getLogger().info(result)
    if result < 0:
        raise BVIException(BVIException.ARCHIVEGEN_FAILED, folder)


def bv_packaging(name, type_, folder):
    """Package a component with no dependency.

    Parameters
    ----------
    name   : package name.
    type_  : type of package: run, doc, usrdoc, devdoc.
    folder : destination full path.
    """
    args = ["%s/%s" % (Paths.BV_BIN, Paths.BV_ENV),
            'python',
            "%s/%s" % (Paths.BV_BIN,Paths.BV_PACKAGING),
            'dir',
            '-o', folder,
            '--wrappers',
            '--no-deps',
            '--installer',
            '+name=%s,type=%s' % (name, type_)]
    subprocess.check_call(args)
