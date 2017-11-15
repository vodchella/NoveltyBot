#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging.handlers
from pkg.constants.date_formats import DATE_FORMAT_FULL
from cfg.external import get_log_path
from cfg.defines import BOT_LOG_FILE_NAME


def create_logger():
    result = logging.getLogger('NoveltyBotLogger')
    result.setLevel(logging.INFO)
    f = logging.Formatter(fmt='%(levelname)s:\t%(asctime)s\t%(message)s', datefmt=DATE_FORMAT_FULL)
    trfh = logging.handlers.TimedRotatingFileHandler(os.path.join(get_log_path(), BOT_LOG_FILE_NAME), 'midnight')
    trfh.setFormatter(f)
    ch = logging.StreamHandler()
    ch.setFormatter(f)
    result.addHandler(trfh)
    result.addHandler(ch)
    return result


BOT_LOGGER = create_logger()
