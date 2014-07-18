
.. highlight: bash


===================
BrainVISA installer
===================


Developers
==========

Building an installer with repository for a complete software distribution
--------------------------------------------------------------------------

* Genral form: including thirdparty dependencies

  ::

      bv_build_installer.py

* For internal distributions, or for a specific system, using the system tools and libraries:

  ::

      bv_build_installer.py --no-thirdparty

For the full brainvisa distribution we have a script with the right projects list:

::

    bv_build_installer_i2bm


Building an installer with custom repository to distribute a set of toolboxes adding to an existing base and repository
-----------------------------------------------------------------------------------------------------------------------

::

    bv_build_installer.py --no-dependencies -p my_project

Add the additional repository in the update tool


Adding new toolboxes to an existing repository
----------------------------------------------

::

    bv_build_installer.py --no-dependencies -p my_project


Updating toolboxes and repositories
-----------------------------------




