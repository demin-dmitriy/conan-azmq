#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile, CMake, tools
import os


class AZMQConan(ConanFile):
    name = 'azmq'
    version = 'a8f54cc8c9672da7d6301fe1d2719b1436ab4816'
    url = 'https://github.com/bincrafters/conan-azmq'
    homepage = 'https://github.com/zeromq/azmq'
    description = 'C++ language binding library integrating ZeroMQ with Boost Asio'
    license = 'BSL-1.0'
    exports = ['LICENSE.md']
    exports_sources = ['CMakeLists.txt']
    generators = 'cmake'
    settings = 'os', 'arch', 'compiler', 'build_type'
    source_subfolder = 'source_subfolder'
    build_subfolder = 'build_subfolder'

    def requirements(self):
        self.requires.add('zmq/4.2.5@bincrafters/stable')
        self.requires.add('boost/1.67.0@conan/stable')

        # It seems that package cmake_findboost_modular doesn't really depend on
        # exact boost version, so it should be okay to use the older one.
        self.requires.add('cmake_findboost_modular/1.66.0@bincrafters/stable')

    def source(self):
        source_url = 'https://codeload.github.com/zeromq/azmq'
        tools.get('{0}/zip/{1}'.format(source_url, self.version))
        extracted_dir = self.name + '-' + self.version
        os.rename(extracted_dir, self.source_subfolder)

        # ensure our FindBoost.cmake is being used
        tools.replace_in_file(
            os.path.join(self.source_subfolder, 'CMakeLists.txt'),
            'set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/config")',
            '#set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/config")'
        )

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions['AZMQ_NO_TESTS'] = True
        cmake.configure(build_folder=self.build_subfolder)
        return cmake
                              
    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy(pattern='LICENSE-BOOST_1_0', dst='licenses', src=self.source_subfolder)

    def package_info(self):
        self.info.header_only()
