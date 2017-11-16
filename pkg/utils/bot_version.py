#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cfg.defines import BOT_VERSION
from pkg.utils.git import get_top_commit


def get_bot_version_str():
    commit = get_top_commit()
    commit_str = '.' + commit if commit else ''
    return 'NoveltyBot v%s%s' % (BOT_VERSION, commit_str)
