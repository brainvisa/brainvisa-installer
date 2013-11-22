#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pprint
import subprocess
from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_utils.system import System


def binarycreator(installer_path, repository_path, online_only=False, 
	offline_only=False, exclude=None, include=None):
	"The binarycreator tool to create offline and online installers"

	param_online_only = ' --online-only' if online_only else ''
	param_offline_only = ' --offline-only' if offline_only else ''
	param_exclude = ' --exclude ' + exclude.join(',') if exclude else ''
	param_include = ' --include ' + include.join('') if include else ''
	param_config = ' -c %s/config/config.xml' % repository_path
	param_packages = ' -p %s/packages' % repository_path

	cmd = "%s %s%s%s%s%s%s %s" % (Paths.IFW_BINARYCREATOR, param_online_only, param_offline_only, 
		param_exclude, param_include, param_config, param_packages, installer_path)
	os.system(cmd)
	# custom_env = os.environ.copy()
	# custom_env['PATH'] = Paths.BVI_SHARE_BIN + ':' + custom_env['PATH']
	# pprint.pprint(args)
	# #process = subprocess.Popen(args, env=custom_env)
	# #process = subprocess.Popen(args, cwd=repository_path, env=custom_env)
	# process = subprocess.Popen(args)
	# result = process.wait()

	# if result < 0:
	# 	message = "Installer path: %s, Repository path: %s." % (installer_path, repository_path)
	# 	raise BVIException(BVIException.BINARYCREATOR_FAILED, message)


def repogen(path_repository_in, path_repository_out, components = None, update=False, exclude=None, updateurl=None):
	"The repogen tool is to generate online repositories"
	param_components = components.join(',') if exclude else ''
	param_update = '--update' if update else ''
	param_exclude = '--exclude ' + exclude.join(',') if exclude else ''
	param_updateurl = '-u %s' % updateurl  if updateurl else ''
	param_packages = "-p %s/packages" % path_repository_in
	param_config = "-c %s/config/config.xml" % path_repository_in
	
	cmd = "%s %s %s %s %s %s %s %s" % (Paths.IFW_REPOGEN, param_config, param_packages, 
		param_update, param_exclude, param_updateurl, param_components, path_repository_out)
	print cmd
	os.system(cmd)


def archivegen(folder):
	"The archivegen tool is to package the files as a 7zip archive"
	args = ['archivegen', 'data.7z', 'data']
	process = subprocess.Popen(args, cwd=folder)
	result = process.wait()
	if result < 0:
		raise BVIException(BVIException.ARCHIVEGEN_FAILED, "%s/data" % folder)


def bv_packaging(name, type_, full_folder):
	args = ['./bv_env ./bv_packaging dir -o %s --no-deps +name=%s,type=%s' % (full_folder, name, type_)]
	process = subprocess.Popen(args, cwd = Paths.BV_BIN, shell=True)
	print "---------------> a"
	result = process.wait()
	print "---------------> b"
	if result < 0:
		raise BVIException(BVIException.PACKAGING_FAILED, folder)
	# print "---------------> a"
	# cmd = '%s/bv_env %s/bv_packaging dir -o %s --no-deps +name=%s,type=%s' % (Paths.BV_BIN, Paths.BV_BIN, full_folder, name, type_)
	# os.system(cmd)
	# print "---------------> b"