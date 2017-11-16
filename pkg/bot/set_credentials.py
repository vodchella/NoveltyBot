#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg.sessions import *
from pkg.bot import bot
from pkg.bot.common import send_menu_main, check_novelty_auth
from pkg.constants.emoji import EMOJI_CROSS_MARK
from pkg.utils.decorators.handle_exceptions import handle_exceptions


@handle_exceptions
def handler_set_credentials(message):
    if message.text:
        lines = message.text.split('\n')
        if len(lines) != 2:
            msg = bot.send_message(message.chat.id,
                                   EMOJI_CROSS_MARK +
                                   ' Я же говорю, на первой строчке логин, а на второй пароль. Давай ещё раз:')
            bot.register_next_step_handler(msg, handler_set_credentials)
        else:
            if check_novelty_auth(message.chat.id, lines[0], lines[1]):
                user_id = message.from_user.id
                create_or_update_session(user_id, lines[0], lines[1])
            send_menu_main(message.chat.id)
