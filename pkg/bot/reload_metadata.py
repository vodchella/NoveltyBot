#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg.sessions import *
from pkg.bot import bot
from pkg.utils.logger import BOT_LOGGER
from pkg.utils.console import get_raised_error
from pkg.connectors.novelty import Novelty
from pkg.constants.emoji import EMOJI_WHITE_HEAVY_CHECK_MARK
from pkg.constants.bot_messages import BOT_MESSAGE_EXCEPTION


def reload_metadata(session, chat_id):
    subdomain = '?'
    server = get_last_server(session)
    if server:
        try:
            bot.send_message(chat_id, 'Начинаю перезагрузку данных на сервере "%s"...' % (server['name']))
            for subdomain in server['subdomains']:
                BOT_LOGGER.info('Пользователь %s перезагружает метаданные на сервере %s' %
                                (session['login'], subdomain))
                with Novelty(subdomain,
                             session['login'],
                             session['password'],
                             raise_errors=True,
                             use_local_addr=True) as ws:
                    if ws.is_authentificated():
                        ws.reload()
                        BOT_LOGGER.info('Пользователь %s успешно перезагрузил метаданные на сервере %s' %
                                        (session['login'], subdomain))
            bot.send_message(chat_id,
                             EMOJI_WHITE_HEAVY_CHECK_MARK +
                             ' Метаданные на сервере "%s" успешно перезагружены' % (server['name']))
        except Exception as e:
            err_str = get_raised_error(full=True)
            BOT_LOGGER.error('Ошибка перезагрузки метаданных пользователем %s на сервере %s:\n%s' %
                             (session['login'], subdomain, err_str))
            bot.send_message(chat_id, BOT_MESSAGE_EXCEPTION + str(e))
