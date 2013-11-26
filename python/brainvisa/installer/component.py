#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import abc
import shutil
import datetime
import os.path

from brainvisa.installer.bvi_utils.tools import archivegen, bv_packaging

from brainvisa.compilation_info import packages_info


class Component(object):
	"""BrainVISA component.

	Component is an abstract class for the component of BrainVISA installer 
	repository. If the BrainVISA component is builded, Component packages
	the data during the creation. 

	The ifwname and ifwpackage methods must be redefined.

	Parameters
	----------
	name : name of component.
	data : True if the component contains data, the data will be packaged 
		   with bv_packaging.
	"""

	__metaclass__ = abc.ABCMeta

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
		if os.path.isdir(path):
			return
		os.mkdir(path)
		self.__package_meta(path)
		if self.data: 
			self.__package_data(path)

	def __init__(self, name, data=False):
		self.name = name
		self.project = None
		self.type = None
		self.version = None
		self.licenses = None
		self.date = None
		self.data = data
		self.__init_infos()
		self.__init_date()
		
	def __init_infos(self):
		"Initialize the component information."
		if self.name in packages_info:
			infos = packages_info[self.name]
			self.project = infos['project']
			self.type = infos['type']
			self.version = infos['version']
			if 'licences' in infos:
				self.licenses = infos['licences']
		else:
			print "[ BVI ]: WARNING no information for %s" % self.name
			self.project = ''
			self.type = 'thirdparty'
			self.version = '1.0'

	def __init_date(self):
		"Initialize the date."
		now = datetime.datetime.now()
		self.date = now.strftime("%Y-%m-%d")

	def __package_meta(self, folder):
		"Create the meta folder of IFW component."
		meta_folder = "%s/meta" % folder
		os.mkdir(meta_folder)
		self.ifwpackage.save("%s/package.xml" % meta_folder)

	def __package_data(self, folder):
		"Create the data folder of IFW component."
		data_folder = "%s/data" % folder
		os.mkdir(data_folder)
		self.__bv_packaging(data_folder)
		#archivegen(folder)
		#self.__clean_data(data_folder)

	def __bv_packaging(self, folder_data):
		"Use bv_packaging to package the component data."
		bv_packaging(self.name, self.type, folder_data)
		readme = "%s/../data.README" % folder_data
		if os.path.isfile(readme):
			os.remove(readme)

	def __clean_data(self, folder_data):
		"Replace the non compress data by the 7zip archive"
		shutil.rmtree(folder_data)
		os.mkdir(folder_data)
		file_src = "%s.7z" % (folder_data)
		file_des = "%s/%s.7z" % (folder_data, self.name.replace('-', '_'))
		shutil.move(file_src, file_des)