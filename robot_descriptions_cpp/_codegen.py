import os
import importlib


def generate_hpp(module_name: str, prefix=None):
    if prefix is None:
        prefix = os.getcwd()
    hpp_dir = os.path.join(prefix, 'generated', 'include', 'robot_descriptions')
    os.makedirs(hpp_dir, exist_ok=True)
    generate_cmake(module_name, prefix)

    MODULE_NAME = module_name.upper()
    hpp_file = open(os.path.join(hpp_dir, module_name + '.hpp'), 'w')
    hpp_file.write('#ifndef ROBOT_DESCRIPTIONS__' + MODULE_NAME + '_HPP_\n')
    hpp_file.write('#define ROBOT_DESCRIPTIONS__' + MODULE_NAME + '_HPP_\n\n')
    hpp_file.write('#include <string> \n\n')
    hpp_file.write('namespace robot_descriptions {\n')
    hpp_file.write('namespace ' + module_name + ' {\n\n')

    module = importlib.import_module('robot_descriptions.'+module_name)
    attributes = dir(module)
    attributes[:] = [e for e in attributes if not e.startswith('_')]
    for e in attributes:
        hpp_file.write('std::string ' + e + '() { return "' + str(getattr(module, e)) + '"; } \n\n')

    hpp_file.write('} // namespace ' + module_name + '\n')
    hpp_file.write('} // namespace robot_descriptions \n\n')
    hpp_file.write('#endif // ROBOT_DESCRIPTIONS__' + MODULE_NAME + '_HPP_\n')


def generate_cmake(module_name: str, prefix=None):
    if prefix is None:
        prefix = os.getcwd()
    cmake_dir = os.path.join(prefix, 'generated')
    os.makedirs(cmake_dir, exist_ok=True)
    cmake_file = open(os.path.join(cmake_dir, 'CMakeLists.txt'), 'w')
    cmake_file.writelines([
"""
cmake_minimum_required(VERSION 3.1)
project(robot_descriptions CXX)

# installation directories
include(GNUInstallDirs)
set(ROBOT_DESCRIPTIONS_INSTALL_CMAKE_DIR "${CMAKE_INSTALL_DATAROOTDIR}/${PROJECT_NAME}/cmake" CACHE STRING "The installation cmake directory")

# the interface library
add_library(${PROJECT_NAME} INTERFACE)
add_library(${PROJECT_NAME}::${PROJECT_NAME} ALIAS ${PROJECT_NAME})
target_include_directories(
  ${PROJECT_NAME} INTERFACE 
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

# cmake configs
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
  ${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake
  VERSION 0.1
  COMPATIBILITY AnyNewerVersion
)
configure_package_config_file(
  ${PROJECT_SOURCE_DIR}/cmake/${PROJECT_NAME}-config.cmake.in
  ${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
  INSTALL_DESTINATION ${ROBOT_DESCRIPTIONS_INSTALL_CMAKE_DIR}
  NO_CHECK_REQUIRED_COMPONENTS_MACRO
  NO_SET_AND_CHECK_MACRO
)

# install files
install(
  TARGETS ${PROJECT_NAME} 
  EXPORT ${PROJECT_NAME}-targets 
)
install(
  FILES ${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config-version.cmake
        ${PROJECT_BINARY_DIR}/${PROJECT_NAME}-config.cmake
  DESTINATION ${ROBOT_DESCRIPTIONS_INSTALL_CMAKE_DIR}
)
install(
  DIRECTORY ${PROJECT_SOURCE_DIR}/include/robot_descriptions
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
# export
export(EXPORT ${PROJECT_NAME}-targets
  FILE ${PROJECT_BINARY_DIR}/${PROJECT_NAME}-targets.cmake
  NAMESPACE robot_descriptions::
)
install(EXPORT ${PROJECT_NAME}-targets
  NAMESPACE robot_descriptions::
  DESTINATION ${ROBOT_DESCRIPTIONS_INSTALL_CMAKE_DIR}
)
"""
    ])

    cmake_dir = os.path.join(cmake_dir, 'cmake')
    os.makedirs(cmake_dir, exist_ok=True)
    cmake_file = open(os.path.join(cmake_dir, 'robot_descriptions-config.cmake.in'), 'w')
    cmake_file.writelines([
"""
@PACKAGE_INIT@

include("${CMAKE_CURRENT_LIST_DIR}/robot_descriptions-targets.cmake")
set("robot_descriptions_INCLUDE_DIR" "@CMAKE_INSTALL_FULL_INCLUDEDIR@")
set("ROBOT_DESCRIPTIONS_INCLUDE_DIR" "@CMAKE_INSTALL_FULL_INCLUDEDIR@")
"""
    ])