#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg.sessions import *
from pkg.bot import bot
from pkg.bot.common import not_authorized, send_menu_main
from pkg.utils.decorators.handle_exceptions import handle_exceptions
from pkg.utils.logger import BOT_LOGGER
from pkg.utils.console import get_raised_error
from pkg.connectors.oracle import Oracle, get_connection_string
from pkg.constants.emoji import EMOJI_CROSS_MARK, EMOJI_WHITE_HEAVY_CHECK_MARK
from pkg.constants.bot_messages import BOT_MESSAGE_EXCEPTION
from pkg.sql.queries import \
    GET_NONEXISTANT_POLICIES, \
    UPDATE_RESCINDING_REASON_TO_NULL, \
    SET_USER_ID, \
    SELECT_TEXT_FROM_DUAL


def unset_rescinding_reason(chat_id):
    msg = bot.send_message(chat_id,
                           'Введи номер тикета, согласно которому необходимо снять причину расторжения с полисов:')
    bot.register_next_step_handler(msg, handler_set_ticket)


@handle_exceptions
def handler_set_ticket(message):
    if len(message.text) != 16:
        msg = bot.send_message(message.chat.id, EMOJI_CROSS_MARK + ' Это не номер тикета. Давай ещё раз:')
        bot.register_next_step_handler(msg, handler_set_ticket)
    else:
        session = get_session(message.from_user.id)
        if session:
            set_last_ticket(session, message.text)
            msg = bot.send_message(message.chat.id, 'Теперь укажи номера полисов, каждый с новой строчки:')
            bot.register_next_step_handler(msg, handler_set_policies)
        else:
            not_authorized(message.chat.id)


@handle_exceptions
def handler_set_policies(message):
    session = get_session(message.from_user.id)
    if session:
        server = get_last_server(session)
        if server:
            connection_string = get_connection_string(server)
            secure_conn_str = get_connection_string(server, secure=True)
            try:
                bot.send_message(message.chat.id, 'Начинаю работу с базой данных...')
                policies = message.text.split('\n')
                policies_str = ', '.join('\'%s\'' % p for p in policies)
                policies_tbl = ' union all '.join(SELECT_TEXT_FROM_DUAL % p for p in policies)
                ticket = get_last_ticket(session)
                BOT_LOGGER.info('Пользователь %s соединяется с БД "%s" (%s)' %
                                (session['login'], server['name'], secure_conn_str))
                with Oracle(connection_string) as db:
                    def get_nonexistant_policies(cur):
                        BOT_LOGGER.info('Пользователь %s ищет несуществующие полисы среди (%s): %s' %
                                        (session['login'], len(policies), policies_str))
                        sql = GET_NONEXISTANT_POLICIES % policies_tbl
                        cur.execute(sql.encode('utf-8'))
                        for row in cur:
                            return row[0], row[1]

                    def erase_policies_rescinding_reason(cur):
                        BOT_LOGGER.info('Пользователь %s обнуляет причину расторжения у полисов: %s' %
                                        (session['login'], policies_str))
                        sql = SET_USER_ID % ('Updated by NoveltyBot; Ticket# %s' % ticket)
                        cur.execute(sql, user_name=session['login'])
                        sql = UPDATE_RESCINDING_REASON_TO_NULL % policies_str
                        cur.execute(sql.encode('utf-8'))
                        return cur.rowcount

                    p_list, p_count = db.execute(get_nonexistant_policies)
                    if p_count:
                        BOT_LOGGER.info('Пользователь %s не нашёл некоторые полисы (%s): %s' %
                                        (session['login'], p_count, policies_str))
                        bot.send_message(message.chat.id,
                                         EMOJI_CROSS_MARK +
                                         ' Некоторые полисы (%s) не найдены: %s' % (p_count, p_list))

                    if p_count == len(policies):
                        p_count = 0
                    else:
                        p_count = db.execute(erase_policies_rescinding_reason)
                    BOT_LOGGER.info('Пользователь %s изменил полисов по тикету %s: %s' %
                                    (session['login'], ticket, p_count))
                    bot.send_message(message.chat.id, EMOJI_WHITE_HEAVY_CHECK_MARK + ' Обновлено полисов: %s' % p_count)

            except Exception as e:
                err_str = get_raised_error(full=True)
                BOT_LOGGER.error('Ошибка при работе с БД %s пользователя %s:\n%s' %
                                 (secure_conn_str, session['login'], err_str))
                bot.send_message(message.chat.id, BOT_MESSAGE_EXCEPTION + str(e))
        send_menu_main(message.chat.id)
    else:
        not_authorized(message.chat.id)
