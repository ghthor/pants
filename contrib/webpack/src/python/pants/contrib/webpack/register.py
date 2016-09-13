# coding=utf-8
# Copyright 2016 Foursquare Labs Inc. All Rights Reserved.

from __future__ import absolute_import

from pants.build_graph.build_file_aliases import BuildFileAliases
from pants.goal.goal import Goal
from pants.goal.task_registrar import TaskRegistrar as task

from pants.contrib.webpack.subsystems.resolvers.webpack_resolver import WebPackResolver
from pants.contrib.webpack.targets.webpack_module import WebPackModule
from pants.contrib.webpack.tasks.webpack import WebPack
from pants.contrib.webpack.tasks.webpack_bundle import WebPackBundle
from pants.contrib.webpack.tasks.webpack_resolve import WebPackResolve


def build_file_aliases():
  return BuildFileAliases(
    targets={
      'webpack_module': WebPackModule,
    },
  )

def global_subsystems():
  return (WebPackResolver,)

def register_goals():

  task(name='webpack', action=WebPack).install()
  task(name='webpack-resolve', action=WebPackResolve).install()
  task(name='webpack-bundle', action=WebPackBundle).install('webpack')
