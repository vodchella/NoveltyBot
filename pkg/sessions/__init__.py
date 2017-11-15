#!/usr/bin/env python3
# -*- coding: utf-8 -*-

sessions = {}


def create_or_update_session(user_id, login, password):
    global sessions
    sessions[user_id] = {
        'telegram_id': user_id,
        'login': login,
        'password': password
    }


def get_session(user_id):
    global sessions
    return sessions.get(user_id)


def set_last_server(session, server):
    if session:
        session['last_server'] = server


def get_last_server(session):
    if session:
        return session['last_server']


def set_last_ticket(session, ticket):
    if session:
        session['last_ticket'] = ticket


def get_last_ticket(session):
    if session:
        return session['last_ticket']
