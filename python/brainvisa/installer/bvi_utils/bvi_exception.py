#!/usr/bin/env python
# -*- coding: utf-8 -*-

# OBSELETE


class BVIException(Exception):

    """Custom exception for BrainVISA Installer.

    The error message can be splited with error and detail parameters.

    Example
    -------
    e = BVIException(BVIException.PROJECT_NONEXISTENT, project_name)
    """

    PROJECT_NONEXISTENT = 'The BrainVISA project does not exist. Check the project name and if the project has been downloaded and builed with brainvisa-cmake.'  # pylint: disable=C0301
    COMPONENT_NONEXISTENT = 'The BrainVISA component does not exist. Perhaps it has not been builed.'  # pylint: disable=C0301
    PACKAGING_FAILED = 'The BrainVISA command bv_packaging failed'
    ARCHIVEGEN_FAILED = 'The IFW command repogen failed'
    BINARYCREATOR_FAILED = 'The IFW commande binarycreator failed'
    DOC_TYPE_INVALID = 'The type doc is not taking into account in BrainVISA Installer, use usrdoc or devdoc type'  # pylint: disable=C0301

    def __init__(self, error, detail=''):
        message = '[ BVI ERROR ] %s: %s.' % (error, detail)
        super(BVIException, self).__init__(message)

    def __str__(self):
        return ' '.join(self.args)
