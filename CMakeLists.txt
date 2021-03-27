cmake_minimum_required(VERSION 3.16.0)

project(zita-resampler VERSION 1.8.0)

option(ZITA_RESAMPLER_TESTS "Build zita-resampler code in test directory" ON)

add_definitions(-DVERSION="${zita-resampler_VERSION}")

set(CMAKE_CPPFLAGS_FLAGS "${CMAKE_CPPFLAGS_FLAGS} -I. -D_REENTRANT -D_POSIX_PTHREAD_SEMANTICS")
set(CMAKE_CXXFLAGS_FLAGS "${CMAKE_CXXFLAGS_FLAGS} -Wall -fPIC -O2 -ffast-math -march=native")

# Source control
set(SOURCES
    source/resampler.cc
    source/vresampler.cc
    source/resampler-table.cc
    source/cresampler.cc
    source/zita-resampler/resampler.h
    source/zita-resampler/resampler-table.h
    source/zita-resampler/vresampler.h
    source/zita-resampler/cresampler.h
)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/source)

# make
add_library(zita-resampler ${SOURCES})

if(WIN32)
    add_definitions(-D_USE_MATH_DEFINES)
    set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_BINARY_DIR}) # This is need to find the conan-generated Findpthreads4w.cmake in the binary output dir
    find_package(pthreads4w REQUIRED)
    set(LIB_THREADS pthreads4w::pthreads4w)
    target_link_libraries(zita-resampler PUBLIC ${LIB_THREADS})
else()
    find_package(Threads REQUIRED)
    set(LIB_THREADS Threads::Threads)
endif()

if(ZITA_RESAMPLER_TESTS)
    # Test exeuctables
    add_executable(zita-resampler-speedtest test/speedtest.cc test/clock_gettime_windows.h)
    target_link_libraries(zita-resampler-speedtest PUBLIC zita-resampler ${LIB_THREADS})

    add_executable(zita-resampler-vspeedtest test/vspeedtest.cc test/clock_gettime_windows.h)
    target_link_libraries(zita-resampler-vspeedtest PUBLIC zita-resampler ${LIB_THREADS})

    add_executable(zita-resampler-upstest test/upstest.cc test/clock_gettime_windows.h)
    target_link_libraries(zita-resampler-upstest PUBLIC zita-resampler ${LIB_THREADS})
endif()

# CMake package config
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
set(generated_dir "${CMAKE_CURRENT_BINARY_DIR}/generated")
set(project_config "${generated_dir}/${PROJECT_NAME}Config.cmake")
set(version_config "${generated_dir}/${PROJECT_NAME}ConfigVersion.cmake")
set(TARGETS_EXPORT_NAME "${PROJECT_NAME}Targets")
set(namespace "${PROJECT_NAME}::")
set(config_install_dir "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}")
set(TARGETS_EXPORT_NAME "${PROJECT_NAME}Targets")
write_basic_package_version_file(
        "${version_config}" COMPATIBILITY SameMajorVersion
)
configure_package_config_file(
        "cmake/Config.cmake.in"
        "${project_config}"
        INSTALL_DESTINATION "${config_install_dir}"
)

# make install
install(
        TARGETS zita-resampler
        EXPORT "${TARGETS_EXPORT_NAME}"
        LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
        ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
        RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
        INCLUDES DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
)
install(
        FILES "${project_config}" "${version_config}"
        DESTINATION "${config_install_dir}"
)
install(
        EXPORT "${TARGETS_EXPORT_NAME}"
        NAMESPACE "${namespace}"
        DESTINATION "${config_install_dir}"
)