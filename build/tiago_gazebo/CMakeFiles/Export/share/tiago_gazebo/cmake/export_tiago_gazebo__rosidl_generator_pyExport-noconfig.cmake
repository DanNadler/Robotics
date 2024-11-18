#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "tiago_gazebo::tiago_gazebo__rosidl_generator_py" for configuration ""
set_property(TARGET tiago_gazebo::tiago_gazebo__rosidl_generator_py APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(tiago_gazebo::tiago_gazebo__rosidl_generator_py PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libtiago_gazebo__rosidl_generator_py.so"
  IMPORTED_SONAME_NOCONFIG "libtiago_gazebo__rosidl_generator_py.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS tiago_gazebo::tiago_gazebo__rosidl_generator_py )
list(APPEND _IMPORT_CHECK_FILES_FOR_tiago_gazebo::tiago_gazebo__rosidl_generator_py "${_IMPORT_PREFIX}/lib/libtiago_gazebo__rosidl_generator_py.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
