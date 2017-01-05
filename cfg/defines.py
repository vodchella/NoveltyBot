#!/usr/bin/env python3
# -*- coding: utf-8 -*-

DEBUG = False

SERVERS = [
    # Тестовые
    {
        'name': 'Тестовый Аско',
        'subdomains': ['testasko']
    },
    {
        'name': 'Тестовый Евразия',
        'subdomains': ['testeur']
    },
    {
        'name': 'Тестовый Интертич',
        'subdomains': ['testinter']
    },
    {
        'name': 'Тестовый Казахмыс',
        'subdomains': ['testkmic']
    },
    {
        'name': 'Тестовый Компетенц',
        'subdomains': ['testkompetenz']
    },
    {
        'name': 'Тестовый Номад',
        'subdomains': ['testnomad']
    },
    {
        'name': 'Тестовый Нурполис',
        'subdomains': ['testnur']
    },
    # Боевые
    {
        'name': 'Аско',
        'subdomains': ['asko', 'asko2']
    },
    {
        'name': 'Евразия',
        'subdomains': ['eur', 'eur2']
    },
    {
        'name': 'Интертич',
        'subdomains': ['inter', 'inter2']
    },
    {
        'name': 'Казахмыс',
        'subdomains': ['kmic', 'kmic2']
    },
    {
        'name': 'Компетенц',
        'subdomains': ['kompetenz', 'kompetenz2']
    },
    {
        'name': 'Номад',
        'subdomains': ['nomad', 'nomad2']
    },
    {
        'name': 'Нурполис',
        'subdomains': ['nur', 'nur2']
    },
    {
        'name': 'Novelty',
        'subdomains': ['home', 'home2']
    }
]

SMB_CRED_FILE = '.smbcredentials'
