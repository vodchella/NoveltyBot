#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cfg.external import SERVERS
from pkg.bot import bot, telebot
from pkg.constants.bot_messages import BOT_MESSAGE_NOT_AUTHORIZED, BOT_MESSAGE_EXCEPTION
from pkg.constants.bot_actions import BOT_ACTIONS_MAIN
from pkg.constants.emoji import EMOJI_WHITE_HEAVY_CHECK_MARK
from pkg.utils.logger import BOT_LOGGER
from pkg.utils.console import get_raised_error
from pkg.connectors.novelty import Novelty


def send_menu_main(chat_id):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*[telebot.types.InlineKeyboardButton(text=name,
                                                      callback_data=data) for (data, name) in BOT_ACTIONS_MAIN])
    bot.send_message(chat_id, 'Что хочешь сделать?', reply_markup=keyboard)


def send_menu_select_server(chat_id, action_id):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        *[telebot.types.InlineKeyboardButton(text=server['name'],
                                             callback_data='%s:%s' % (server['id'], action_id)) for server in SERVERS])
    bot.send_message(chat_id, 'Выбери сервер:', reply_markup=keyboard)


def not_authorized(chat_id):
    bot.send_message(chat_id, BOT_MESSAGE_NOT_AUTHORIZED)
    send_menu_main(chat_id)


def check_novelty_auth(chat_id, session, server):
    subdomain = '?'
    try:
        subdomain = server['subdomains'][0]
        BOT_LOGGER.info('Пользователь %s авторизируется на сервере %s' %
                        (session['login'], subdomain))
        bot.send_message(chat_id, 'Пытаюсь авторизироваться в Novelty...')
        with Novelty(subdomain,
                     session['login'],
                     session['password'],
                     raise_errors=True,
                     use_local_addr=True) as ws:
            if ws.is_authentificated():
                bot.send_message(chat_id,
                                 EMOJI_WHITE_HEAVY_CHECK_MARK +
                                 ' Авторизация прошла успешно')
                BOT_LOGGER.info('Пользователь %s успешно авторизировался на сервере %s' %
                                (session['login'], subdomain))
                return True
    except Exception as e:
        err_str = get_raised_error(full=True)
        BOT_LOGGER.error('Ошибка при авторизации пользователя %s на сервере %s:\n%s' %
                         (session['login'], subdomain, err_str))
        bot.send_message(chat_id, BOT_MESSAGE_EXCEPTION + str(e))
        return False
