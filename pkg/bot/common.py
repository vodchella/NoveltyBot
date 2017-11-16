#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cfg.external import SERVERS, get_ldap_settings
from pkg.bot import bot, telebot
from pkg.constants.bot_messages import BOT_MESSAGE_NOT_AUTHORIZED, BOT_MESSAGE_EXCEPTION
from pkg.constants.bot_actions import BOT_ACTIONS_MAIN
from pkg.constants.emoji import EMOJI_WHITE_HEAVY_CHECK_MARK, EMOJI_NO_ENTRY
from pkg.utils.logger import BOT_LOGGER
from pkg.utils.console import get_raised_error
from pkg.utils.bot_version import get_bot_version_str
from pkg.connectors.ldap import Ldap


def send_menu_main(chat_id, greeting=False):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*[telebot.types.InlineKeyboardButton(text=name,
                                                      callback_data=data) for (data, name) in BOT_ACTIONS_MAIN])
    greeting_msg = '%s приветствует тебя!\n' % get_bot_version_str() if greeting else ''
    bot.send_message(chat_id, greeting_msg + 'Что хочешь сделать?', reply_markup=keyboard)


def send_menu_select_server(chat_id, action_id):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        *[telebot.types.InlineKeyboardButton(text=server['name'],
                                             callback_data='%s:%s' % (server['id'], action_id)) for server in SERVERS])
    bot.send_message(chat_id, 'Выбери сервер:', reply_markup=keyboard)


def not_authorized(chat_id):
    bot.send_message(chat_id, BOT_MESSAGE_NOT_AUTHORIZED)
    send_menu_main(chat_id)


def check_novelty_auth(chat_id, login, password):
    settings = get_ldap_settings()
    ldap_uri = 'ldap://%s:%s' % (settings[0], settings[1])
    try:
        BOT_LOGGER.info('Авторизация пользователя %s на %s' % (login, ldap_uri))
        bot.send_message(chat_id, 'Пытаюсь авторизироваться в Novelty...')
        with Ldap(settings[0], settings[1], settings[2], login, password) as lconn:
            auth_result = lconn.auth()
            if auth_result[0]:
                bot.send_message(chat_id,
                                 EMOJI_WHITE_HEAVY_CHECK_MARK +
                                 ' Авторизация прошла успешно')
                BOT_LOGGER.info('Пользователь %s успешно авторизировался на %s' % (login, ldap_uri))
                return True
            else:
                bot.send_message(chat_id,
                                 EMOJI_NO_ENTRY +
                                 ' Не удалось авторизироваться: ' + auth_result[1])
                BOT_LOGGER.error('Не удалось авторизировать пользователя %s на %s: %s' %
                                 (login, ldap_uri, auth_result[1]))
                return False
    except Exception as e:
        err_str = get_raised_error(full=True)
        BOT_LOGGER.error('Ошибка при авторизации пользователя %s на %s:\n%s' %
                         (login, ldap_uri, err_str))
        bot.send_message(chat_id, BOT_MESSAGE_EXCEPTION + str(e))
        return False


def check_novelty_auth_by_session(chat_id, session):
    return check_novelty_auth(chat_id, session['login'], session['password'])
