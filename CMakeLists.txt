cmake_minimum_required( VERSION 2.6 )
find_package( brainvisa-cmake REQUIRED )
BRAINVISA_PROJECT()

find_package( python REQUIRED )
find_package( PyQt4 REQUIRED )


BRAINVISA_DEPENDENCY( RUN DEPENDS python RUN ">= ${PYTHON_SHORT_VERSION}" )
BRAINVISA_DEPENDENCY( DEV DEPENDS python DEV ">= 2.4;<< 3.0" )
BRAINVISA_DEPENDENCY( RUN DEPENDS python-qt4 RUN )
BRAINVISA_DEPENDENCY( DEV DEPENDS python-qt4 DEV )

BRAINVISA_COPY_PYTHON_DIRECTORY( "${CMAKE_CURRENT_SOURCE_DIR}/python"
                                 ${PROJECT_NAME} )
BRAINVISA_COPY_DIRECTORY( "${CMAKE_CURRENT_SOURCE_DIR}/bin"
                          bin
                          ${PROJECT_NAME} )

BRAINVISA_CREATE_CMAKE_CONFIG_FILES()


