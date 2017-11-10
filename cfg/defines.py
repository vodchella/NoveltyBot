#!/usr/bin/env python3
# -*- coding: utf-8 -*-

DEBUG = False

SERVERS = [
    # Тестовые
    {
        'id': 'server_id_01',
        'name': 'Тестовый Аско',
        'subdomains': ['testasko']
    },
    {
        'id': 'server_id_02',
        'name': 'Тестовый Евразия',
        'subdomains': ['testeur']
    },
    {
        'id': 'server_id_03',
        'name': 'Тестовый Интертич',
        'subdomains': ['testinter']
    },
    {
        'id': 'server_id_04',
        'name': 'Тестовый Компетенц',
        'subdomains': ['testkompetenz']
    },
    {
        'id': 'server_id_05',
        'name': 'Тестовый Номад',
        'subdomains': ['testnomad']
    },
    {
        'id': 'server_id_06',
        'name': 'Тестовый Нурполис',
        'subdomains': ['testnur']
    },
    # Боевые
    {
        'id': 'server_id_07',
        'name': 'Аско',
        'subdomains': ['asko', 'asko2']
    },
    {
        'id': 'server_id_08',
        'name': 'Евразия',
        'subdomains': ['eur', 'eur2']
    },
    {
        'id': 'server_id_09',
        'name': 'Интертич',
        'subdomains': ['inter', 'inter2']
    },
    {
        'id': 'server_id_10',
        'name': 'Компетенц',
        'subdomains': ['kompetenz', 'kompetenz2']
    },
    {
        'id': 'server_id_11',
        'name': 'Номад',
        'subdomains': ['nomad', 'nomad2']
    },
    {
        'id': 'server_id_12',
        'name': 'Нурполис',
        'subdomains': ['nur', 'nur2']
    },
    {
        'id': 'server_id_13',
        'name': 'Novelty',
        'subdomains': ['home', 'home2']
    }
]

SMB_CRED_FILE = '.smbcredentials'
PID_FILE = 'novelty_telegram_bot'
BOT_TOKEN_FILE = '.novelty_telegram_bot_token'

BOT_ACTION_SET_CREDENTIALS = '1'
BOT_ACTION_RELOAD_METADATA = '2'

BOT_ACTIONS_MAIN = [
    (BOT_ACTION_SET_CREDENTIALS, 'Задать логин и пароль'),
    (BOT_ACTION_RELOAD_METADATA, 'Перезагрузить метаданные')
]
