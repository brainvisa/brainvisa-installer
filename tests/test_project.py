#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os.path
import datetime
import collections
from brainvisa.installer.project import Project
from brainvisa.installer.bvi_xml.configuration import Configuration
from brainvisa.maker.brainvisa_projects_versions import project_description

FULLPATH = os.path.dirname(os.path.abspath(__file__))
CURRENTDATE = datetime.datetime.now().strftime("%Y-%m-%d")


def test_Project_ifwname():
    x = Configuration("%s/in/configuration.xml" % FULLPATH)
    y = Project('anatomist', x)
    y.type = 'run'
    assert y.ifwname == 'brainvisa.app.anatomist'
    y.type = 'usrdoc'
    assert y.ifwname == 'brainvisa.app.anatomist'
    y.type = 'dev'
    assert y.ifwname == 'brainvisa.dev.anatomist'
    y.type = 'devdoc'
    assert y.ifwname == 'brainvisa.dev.anatomist'


def test_iProject_fwpackage():
    x = Configuration()
    y = Project('anatomist', x)
    y.type = 'run'
    p = y.ifwpackage
    assert p.DisplayName == 'Anatomist'
    assert p.Description == project_description('anatomist')
    assert p.Version == '4.5.0'
    assert p.ReleaseDate == CURRENTDATE
    assert p.Name == 'brainvisa.app.anatomist'
    assert p.Virtual == 'false'


def test_Project_init():
    x = Configuration("%s/in/configuration.xml" % FULLPATH)
    y = Project('anatomist', x)
    assert y.name == 'anatomist'
    assert y.project == 'anatomist'
    assert y.types == ['run', 'usrdoc', 'dev', 'devdoc']
    assert y.type == None
    assert y.configuration == x
    assert y.licenses == None
    assert y.data == None
    assert y.dep_packages == collections.defaultdict(list)
    assert y.version == '4.5.0'
    #y.create("%s/out" % FULLPATH)


def test_Project__create_subcategorie():
    x = Configuration("%s/in/configuration.xml" % FULLPATH)
    y = Project('anatomist', x)
    for y.type in y.types:
        y._Project__create_subcategorie("%s/out" % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.app.anatomist.run' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.app.anatomist.run/meta' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.app.anatomist.usrdoc' % FULLPATH)
    assert os.path.isdir(
        '%s/out/brainvisa.app.anatomist.usrdoc/meta' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.dev.anatomist.dev' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.dev.anatomist.dev/meta' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.dev.anatomist.devdoc' % FULLPATH)
    assert os.path.isdir(
        '%s/out/brainvisa.dev.anatomist.devdoc/meta' % FULLPATH)
    assert os.path.isfile(
        '%s/out/brainvisa.app.anatomist.run/meta/package.xml' % FULLPATH)
    assert os.path.isfile(
        '%s/out/brainvisa.app.anatomist.usrdoc/meta/package.xml' % FULLPATH)
    assert os.path.isfile(
        '%s/out/brainvisa.dev.anatomist.dev/meta/package.xml' % FULLPATH)
    assert os.path.isfile(
        '%s/out/brainvisa.dev.anatomist.devdoc/meta/package.xml' % FULLPATH)

    filename = '%s/out/brainvisa.app.anatomist.run/meta/package.xml' % FULLPATH
    assert '<DisplayName>%s</DisplayName>' % x.category_by_id(
        'run').Name in open(filename, 'r').read()
    assert '<Name>brainvisa.app.anatomist.run</Name>' in open(
        filename, 'r').read()
    assert '<Version>4.5.0</Version>' in open(filename, 'r').read()
    assert '<ReleaseDate>%s</ReleaseDate>' % CURRENTDATE in open(
        filename, 'r').read()


def test_Project_create():
    x = Configuration("%s/in/configuration.xml" % FULLPATH)
    y = Project('axon', x)
    y.create('%s/out' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.app.axon.run' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.app.axon.run/meta' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.app.axon.usrdoc' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.app.axon.usrdoc/meta' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.dev.axon.dev' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.dev.axon.dev/meta' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.dev.axon.devdoc' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.dev.axon.devdoc/meta' % FULLPATH)

    assert os.path.isdir('%s/out/brainvisa.app.axon' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.app.axon/meta' % FULLPATH)
    assert os.path.isfile(
        '%s/out/brainvisa.app.axon/meta/package.xml' % FULLPATH)

    filename = '%s/out/brainvisa.app.axon/meta/package.xml' % FULLPATH
    assert '<DisplayName>Axon</DisplayName>' in open(filename, 'r').read()
    assert '<Name>brainvisa.app.axon</Name>' in open(filename, 'r').read()
    assert '<Version>4.5.0</Version>' in open(filename, 'r').read()
    assert '<ReleaseDate>%s</ReleaseDate>' % CURRENTDATE in open(
        filename, 'r').read()

    assert os.path.isdir('%s/out/brainvisa.app.thirdparty.graphviz' % FULLPATH)
    assert os.path.isdir(
        '%s/out/brainvisa.dev.axon.devdoc.axon_devdoc' % FULLPATH)
    assert os.path.isdir('%s/out/brainvisa.app.soma.run.soma_qtgui' % FULLPATH)

    assert os.path.isfile(
        '%s/out/brainvisa.app.aims.run.aims_free/data/bin/AimsAttributedViewer' % FULLPATH)
    assert os.path.isfile(
        '%s/out/brainvisa.app.aims.run.aims_free/data/bin/AimsClosing' % FULLPATH)
    assert os.path.isfile(
        '%s/out/brainvisa.app.aims.run.aims_free/data/bin/AimsElevationMap' % FULLPATH)
    assert os.path.isfile(
        '%s/out/brainvisa.app.aims.run.aims_free/data/bin/AimsImageScaleSpace' % FULLPATH)
