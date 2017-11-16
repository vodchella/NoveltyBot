#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg.utils.modules import import_nonstandart_module
sh = import_nonstandart_module('sh')

git = None
try:
    from sh import git
except:
    pass


def get_top_commit(short=True):
    if git:
        try:
            commit = git('rev-parse', '--short', 'HEAD') if short else git('rev-parse', 'HEAD')
            return commit.strip('\n')
        except:
            pass
