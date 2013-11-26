#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

__author__ = "Hakim Taklanti"
__copyright__ = "Copyright 2013, CEA / Saclay"
__credits__ = ["Hakim Taklanti", "Yann Cointepas", "Denis Rivière", "Nicolas Souedet"]
__license__ = "CeCILL V2"
__version__ = "0.1"
__maintainer__ = "Hakim Taklanti"
__email__ = "hakim.taklanti@altran.com"
__status__ = "dev"


import os.path
import argparse

from brainvisa.installer.project import Project
from brainvisa.installer.package import Package
from brainvisa.installer.repository import Repository
from brainvisa.installer.bvi_utils.paths import Paths
from brainvisa.installer.bvi_xml.configuration import Configuration
from brainvisa.installer.bvi_utils.bvi_exception import BVIException
from brainvisa.installer.bvi_utils.tools import repogen, binarycreator

from brainvisa.maker.brainvisa_projects import brainvisaProjects, brainvisaComponentsPerProject
from brainvisa.compilation_info import packages_info

#-----------------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------------

DESCRIPTION = '''BrainVISA Build Installer allows to build:
  - an offline installer binary that contains all specified BrainVISA packages and the dependencies;
  - an online installer binary and a repository.
'''

EPIGOG = '''
Remarks:
If the option --only-offline is specified then -r/--repository will be ignored.

Examples:
> ./bv_build_installer.py -p soma,aims,anatomist,axon -i $HOME/brainvisa/installer -r $HOME/brainvisa/repository

> ./bv_build_installer.py

'''

#-----------------------------------------------------------------------------
# Methods
#-----------------------------------------------------------------------------

def main():
	"""Main method of BrainVISA Installer.

	It parses the arguments and create the repository and the installer binaries.
	"""

	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=DESCRIPTION,
		epilog=EPIGOG)
	
	parser.add_argument('-p', '--projects',
		type=valid_projects,  
		nargs='+', 
		metavar='project', 
		help='Projects to include in the installer and the repository')

	parser.add_argument('-n', '--names',
		type=valid_names,
		nargs='+', 
		metavar='name', 
		help='Package\'s names to include in the installer and the repository')

	parser.add_argument('-t', '--types', 
		nargs='+', 
		choices=['run', 'dev', 'usrdoc', 'devdoc'], 
		default=['run', 'dev', 'usrdoc', 'devdoc'],
		metavar='name', 
		help='Package\'s types (run, dev, doc, devdoc)')

	parser.add_argument('--only-online', 
		action='store_true', 
		help='Create only an online installer')

	parser.add_argument('--only-offline', 
		action='store_true', 
		help='Create only an offline installer')

	parser.add_argument('--only-repository', 
		action='store_true', 
		help='Create only the repository for the onfline installer')

	parser.add_argument('-i', '--installer', 
		default='BrainVISA_Suite-Installer', 
		metavar='file', 
		help='Installer name (the extension \'_offline\' and \'_online\' will\
		 be added for the offline and online installer.')

	parser.add_argument('-r', '--repository', 
		default=None, 
		metavar='dir', 
		help='Repository name (by default: \'repository\')')

	parser.add_argument('-c', '--config', 
		type=valid_config, 
		default=None, 
		metavar='file', 
		help='Configuration XML file')

	parser.add_argument('-v', '--version',
		action='version',
		version='%(prog)s [' + __status__ + '] - ' + __version__,
		help='Configuration XML file')

	# try:
	args = parser.parse_args()
	
	if args.only_offline:
		return

	config = Configuration(alt_filename = args.config)
	components = list()
	if args.projects:
		for project in args.projects:
			components.append(Project(project, config, args.types))
	if args.names:
		for name in args.names:
			components.append(Package(name))
	if args.repository:
		rep = Repository(
			folder="%s_tmp" % args.repository, 
			components=components, 
			configuration=config)
		print "Create repository..."
		rep.create()
		repogen("%s_tmp" % args.repository, args.repository, update=True)
		if not args.only_repository:
			print "Create installer binary"
			binarycreator(args.installer, args.repository, 
				online_only= args.only_online, 
				offline_only= args.only_offline)
	# except ValueError as e:
	# 	print e.value
	# except BVIException as e:
	# 	print e.value
	# finally:
	# 	print "BrainVISA Build Installer failed!"
	# 	exit(1)

def valid_projects(arg):
	"Check if the project exists."
	if not arg in brainvisaProjects:
		raise BVIException(BVIException.PROJECT_NONEXISTENT, arg)
	else:
		for component in brainvisaComponentsPerProject[arg]:
			valid_names(component)
	return arg

def valid_names(arg):
	"Check if the component exists."
	if not arg in packages_info:
		raise BVIException(BVIException.COMPONENT_NONEXISTENT, arg)
	return arg

def valid_config(arg):
	"Check if the config file exist."
	if not os.path.isfile(arg):
		raise ValueError("%s does not exist!" % arg)
	return arg

if __name__ == "__main__":
	"Entry point of BrainVISA Installer."
	main()