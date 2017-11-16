#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tempfile
import os
from cfg.defines import BOT_PID_FILE
from pkg.utils.modules import import_nonstandart_module
from pkg.utils.logger import BOT_LOGGER
from pkg.utils.bot_version import get_bot_version_str
from pkg.bot.callback_handlers import *

pid = import_nonstandart_module('pid')


@bot.message_handler(commands=['start'])
def handler_start(message):
    send_menu_main(message.chat.id, True)


if __name__ == '__main__':
    os.environ['NLS_LANG'] = 'Russian.AL32UTF8'
    with pid.PidFile(BOT_PID_FILE, piddir=tempfile.gettempdir()):
        BOT_LOGGER.info('%s начал работу' % get_bot_version_str())
        BOT_LOGGER.info('ORACLE_HOME: %s' %
                        (os.environ['ORACLE_HOME'] if 'ORACLE_HOME' in os.environ else None))
        BOT_LOGGER.info('LD_LIBRARY_PATH: %s' %
                        (os.environ['LD_LIBRARY_PATH'] if 'LD_LIBRARY_PATH' in os.environ else None))
        bot.polling(none_stop=True)
