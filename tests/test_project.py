
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import os.path
from brainvisa.installer.project import Project
from brainvisa.installer.bvi_xml.configuration import Configuration

FULLPATH = os.path.dirname(os.path.abspath(__file__))

def test_Project():
	x = Configuration()
	y = Project('anatomist', x)
	y.create("%s/out" % FULLPATH)