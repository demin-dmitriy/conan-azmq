#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bincrafters import build_template_default

if __name__ == "__main__":

    builder = build_template_default.get_builder()

    filtered_builds = []
    for settings, options, env_vars, build_requires, reference in builder.items:
        if settings['compiler'] == 'gcc':
            if settings['compiler.libcxx'] == 'libstdc++11':
                filtered_builds.append([settings, options, env_vars, build_requires])
        else:
            filtered_builds.append([settings, options, env_vars, build_requires])
    builder.builds = filtered_builds

    builder.run()
