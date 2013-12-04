#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Procedures to simplify the use of external tools.
#

import os
import subprocess

from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_utils.bvi_exception import BVIException


def binarycreator(installer_path, repository_path, online_only=False, 
	offline_only=False, exclude=None, include=None):
	"""The binarycreator tool creates an IFW installer.

	Parameters
	----------
	installer_path  : full path of installer binary.
	repository_path : full path of temporary repository.
	online_only 	: True if the installer is only online (default False).
	offline_only 	: True if the installer is only offline (default False).
	exclude 		: list of excluded package's names (default None).
	include 		: list of included package's names (default None).
	"""

	param_online_only = ' --online-only' if online_only else ''
	param_offline_only = ' --offline-only' if offline_only else ''
	param_exclude = ' --exclude ' + exclude.join(',') if exclude else ''
	param_include = ' --include ' + include.join('') if include else ''
	param_config = ' -c %s/config/config.xml' % repository_path
	param_packages = ' -p %s/packages' % repository_path

	cmd = "%s %s%s%s%s%s%s %s" % (Paths.IFW_BINARYCREATOR, 
		param_online_only, 
		param_offline_only, 
		param_exclude, 
		param_include, 
		param_config, 
		param_packages, 
		installer_path)
	os.system(cmd)


def repogen(path_repository_in, path_repository_out, 
	components = None, update=False, exclude=None, 
	updateurl=None): #pylint: disable=R0913
	"""The repogen tool generates an online IFW repositoriy.

	Parameters
	----------
	path_repository_in  : full path of temporary repository.
	path_repository_out : full path of IFW repository.
	components 			: additional components (default None).
	update 				; True if the existing IFW repository must be updated.
	exclude 			: list of excluded package's names (default None).
	updateurl 			: update the URL.
	"""
	param_components = components.join(',') if exclude else ''
	param_update = '--update' if update else ''
	param_exclude = '--exclude ' + exclude.join(',') if exclude else ''
	param_updateurl = '-u %s' % updateurl  if updateurl else ''
	param_packages = "-p %s/packages" % path_repository_in
	param_config = "-c %s/config/config.xml" % path_repository_in
	
	cmd = "%s %s %s %s %s %s %s %s" % (
		Paths.IFW_REPOGEN, 
		param_config, 
		param_packages, 
		param_update, 
		param_exclude, 
		param_updateurl, 
		param_components, 
		path_repository_out)
	os.system(cmd)


def archivegen(folder):
	"""The archivegen tool compresses the files in folder as a 7zip archive.

	The archive will have the same name what the folder with the 7z extension.
	
	Parameter
	---------
	folder - folder with data which must be compressed. 
	"""
	args = ['archivegen', 'data.7z', 'data']
	process = subprocess.Popen(args, cwd=folder)
	result = process.wait()
	if result < 0:
		raise BVIException(BVIException.ARCHIVEGEN_FAILED, "%s/data" % folder)


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
			'-o %s' % folder,
			'--bv_env',
			'--no-deps',
			'+name=%s,type=%s' % (name, type_)]
	os.system(' '.join(args))