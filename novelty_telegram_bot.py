#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cfg.external import get_bot_token
from cfg.defines import BOT_ACTIONS_MAIN, BOT_ACTION_SET_CREDENTIALS, BOT_ACTION_RELOAD_METADATA
from cfg.defines import SERVERS
from pkg.connectors.novelty import Novelty
from pkg.utils.modules import import_nonstandart_module
from pkg.utils.console import write_stdout
telebot = import_nonstandart_module('telebot')


bot = telebot.TeleBot(get_bot_token())
sessions = {}


def get_session(user_id):
    global sessions
    return sessions.get(user_id)


def send_menu_main(chat_id):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*[telebot.types.InlineKeyboardButton(text=name,
                                                      callback_data=data) for (data, name) in BOT_ACTIONS_MAIN])
    bot.send_message(chat_id, 'Что хочешь сделать?', reply_markup=keyboard)


def send_menu_select_server(chat_id):
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*[telebot.types.InlineKeyboardButton(text=server['name'],
                                                      callback_data=server['id']) for server in SERVERS])
    bot.send_message(chat_id, 'Выбери сервер:', reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def handler_start(message):
    send_menu_main(message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data in [BOT_ACTION_SET_CREDENTIALS, BOT_ACTION_RELOAD_METADATA])
def handler_main_menu_commands(c):
    if c.data == BOT_ACTION_SET_CREDENTIALS:
        msg = bot.send_message(c.message.chat.id, 'На первой строке введи логин, а на второй пароль:')
        bot.register_next_step_handler(msg, handler_set_credentials)
    elif c.data == BOT_ACTION_RELOAD_METADATA:
        send_menu_select_server(c.message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data[:9] == 'server_id')
def handler_select_server(c):
    session = get_session(c.from_user.id)
    if session:
        servers = list(filter(lambda s: s['id'] == c.data, SERVERS))
        if servers:
            server = servers[0]
            try:
                bot.send_message(c.message.chat.id,
                                 'Начинаю перезагрузку данных на сервере "%s"...' % (server['name']))
                for subdomain in server['subdomains']:
                    with Novelty(subdomain, session['login'], session['password'], raise_errors=True) as ws:
                        if ws.is_authentificated():
                            ws.reload()
                bot.send_message(c.message.chat.id,
                                 'Метаданные на сервере "%s" успешно перезагружены' % (server['name']))
            except Exception as e:
                bot.send_message(c.message.chat.id, 'Возникла ошибка:\n' + str(e))
    else:
        bot.send_message(c.message.chat.id, 'Ты забыл задать логин и пароль')
    send_menu_main(c.message.chat.id)


def handler_set_credentials(message):
    global sessions
    lines = message.text.split('\n')
    if len(lines) != 2:
        msg = bot.send_message(message.chat.id,
                               'Я же говорю, на первой строчке логин, а на второй пароль. Давай ещё раз:')
        bot.register_next_step_handler(msg, handler_set_credentials)
    else:
        user_id = message.from_user.id
        sessions[user_id] = {
            'telegram_id': user_id,
            'login': lines[0],
            'password': lines[1]
        }
        bot.send_message(message.chat.id, 'Отлично, данные для авторизации приняты!')
        send_menu_main(message.chat.id)


if __name__ == '__main__':
    write_stdout('Бот начал работу...')
    bot.polling(none_stop=True)
