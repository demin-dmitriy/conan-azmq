#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from conans import ConanFile, CMake, tools
import os


class AZMQConan(ConanFile):
    name = "azmq"
    version = "1.0.2"
    url = "https://github.com/bincrafters/conan-azmq"
    description = "Keep it short"
    license = "BSL"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"

    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    def requirements(self):
        self.requires.add('zmq/[>=4.2.2]@bincrafters/stable')
        self.requires.add('boost_system/[>=1.66.0]@bincrafters/stable')
        self.requires.add('boost_log/[>=1.66.0]@bincrafters/stable')
        self.requires.add('boost_date_time/[>=1.66.0]@bincrafters/stable')
        self.requires.add('boost_thread/[>=1.66.0]@bincrafters/stable')
        self.requires.add('boost_chrono/[>=1.66.0]@bincrafters/stable')
        self.requires.add('boost_regex/[>=1.66.0]@bincrafters/stable')
        self.requires.add('boost_random/[>=1.66.0]@bincrafters/stable')
        self.requires.add('boost_asio/[>=1.66.0]@bincrafters/stable')
        self.requires.add("cmake_findboost_modular/[>=1.66.0]@bincrafters/stable")

    def source(self):
        source_url = "https://github.com/zeromq/azmq"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        os.rename(extracted_dir, self.source_subfolder)

        # ensure our FindBoost.cmake is being used
        tools.replace_in_file(os.path.join(self.source_subfolder, 'CMakeLists.txt'),
                              'set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/config")',
                              '#set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/config")')

        # disable tests, 1.0.2 doesn't have AZMQ_NO_TESTS yet...
        tools.replace_in_file(os.path.join(self.source_subfolder, 'CMakeLists.txt'),
                              'add_subdirectory(test)',
                              '#add_subdirectory(test)')
        tools.replace_in_file(os.path.join(self.source_subfolder, 'CMakeLists.txt'),
                              'add_subdirectory(doc)',
                              '#add_subdirectory(doc)')

    def build(self):
        if self.settings.compiler == 'Visual Studio':
            with tools.vcvars(self.settings, force=True, filter_known_paths=False):
                self.build_cmake()
        else:
            self.build_cmake()

    def build_cmake(self):
        cmake = CMake(self, generator='Ninja')
        cmake.configure(build_folder=self.build_subfolder)
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE-BOOST_1_0", dst='license', src=self.source_subfolder)

    def package_info(self):
        self.info.header_only()
