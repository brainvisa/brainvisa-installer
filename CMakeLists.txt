cmake_minimum_required( VERSION 2.6 )

find_package( brainvisa-cmake REQUIRED )
BRAINVISA_PROJECT()

find_package( python REQUIRED )


BRAINVISA_DEPENDENCY( RUN DEPENDS python RUN ">= ${PYTHON_SHORT_VERSION}" )
BRAINVISA_DEPENDENCY( DEV DEPENDS python DEV ">= 2.4;<< 3.0" )

BRAINVISA_COPY_PYTHON_DIRECTORY( "${CMAKE_CURRENT_SOURCE_DIR}/python"
                                 ${PROJECT_NAME} )
BRAINVISA_COPY_DIRECTORY( "${CMAKE_CURRENT_SOURCE_DIR}/bin"
                          bin
                          ${PROJECT_NAME} )
BRAINVISA_COPY_DIRECTORY( "${CMAKE_CURRENT_SOURCE_DIR}/share"
                          share
                          ${PROJECT_NAME} )

configure_file( "${CMAKE_CURRENT_SOURCE_DIR}/config/version.py.in" "${CMAKE_BINARY_DIR}/python/brainvisa/installer/version.py" @ONLY )
BRAINVISA_INSTALL( FILES "${CMAKE_BINARY_DIR}/python/brainvisa/installer/version.py"
                   DESTINATION "python/brainvisa/installer"
                   COMPONENT ${PROJECT_NAME} )

# BRAINVISA_CREATE_CMAKE_CONFIG_FILES()

find_package( Sphinx )

if( SPHINX_FOUND )

    BRAINVISA_GENERATE_SPHINX_DOC( "doc/sphinx"
      "share/doc/brainvisa-installer-${BRAINVISA_PACKAGE_VERSION_MAJOR}.${BRAINVISA_PACKAGE_VERSION_MINOR}" )

endif()

