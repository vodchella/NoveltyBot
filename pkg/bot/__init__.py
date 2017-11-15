#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cfg.external import get_bot_token
from pkg.utils.modules import import_nonstandart_module

telebot = import_nonstandart_module('telebot')
bot = telebot.TeleBot(get_bot_token())
