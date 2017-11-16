#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cfg.external import SERVERS
from pkg.sessions import *
from pkg.bot import bot
from pkg.bot.common import send_menu_main, send_menu_select_server, check_novelty_auth_by_session, not_authorized
from pkg.bot.reload_metadata import reload_metadata
from pkg.bot.unset_rescinding_reason import unset_rescinding_reason
from pkg.bot.set_credentials import handler_set_credentials
from pkg.utils.decorators.handle_exceptions import handle_exceptions
from pkg.constants.bot_actions import *


@bot.callback_query_handler(func=lambda c: c.data in [BOT_ACTION_SET_CREDENTIALS,
                                                      BOT_ACTION_RELOAD_METADATA,
                                                      BOT_ACTION_UNSET_RESCINDING_REASON])
@handle_exceptions
def handler_main_menu_commands(c):
    if c.data == BOT_ACTION_SET_CREDENTIALS:
        msg = bot.send_message(c.message.chat.id, 'На первой строке введи логин, а на второй пароль:')
        bot.register_next_step_handler(msg, handler_set_credentials)
    else:
        send_menu_select_server(c.message.chat.id, c.data)


@bot.callback_query_handler(func=lambda c: c.data[:9] == 'server_id')
@handle_exceptions
def handler_select_server(c):
    session = get_session(c.from_user.id)
    if session:
        server_id = c.data[:12]
        action_id = c.data[13:]
        servers = list(filter(lambda s: s['id'] == server_id, SERVERS))
        if servers:
            server = servers[0]
            set_last_server(session, server)
            if check_novelty_auth_by_session(c.message.chat.id, session):
                if action_id == BOT_ACTION_RELOAD_METADATA:
                    reload_metadata(session, c.message.chat.id)
                    send_menu_main(c.message.chat.id)
                elif action_id == BOT_ACTION_UNSET_RESCINDING_REASON:
                    unset_rescinding_reason(c.message.chat.id)

    else:
        not_authorized(c.message.chat.id)
