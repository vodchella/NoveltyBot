#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pkg.utils.http import request
from cfg.defines import BASE_URLS


class Novelty:
    subdomain = None
    session_id = None

    def __init__(self, subdomain):
        self.subdomain = subdomain

    def login(self, user, password):
        resp = request(BASE_URLS['request_handler'] % self.subdomain,
                       {
                           'login': user,
                           'pwd': password,
                           # Закомментированные параметры — для web-метода login
                           # 'time': int(time.time() * 1000),
                           # 'timeOffset': 360,
                           # 'clear': 0,
                           'RequestType': 'authenticate'
                       },
                       return_resp_obj=True)
        if resp:
            arr = [t[1] for t in resp.info().items() if t[0] == 'Set-Cookie']
            self.session_id = [s[s.find('=') + 1:s.find(';')] for s in arr if 'web_session_id' in s][0]
            return self.session_id

    def logout(self):
        request(BASE_URLS['request_handler'] % self.subdomain,
                {'RequestType': 'logout'},
                headers={'Cookie': 'web_session_id=%s' % self.session_id})

    def reload(self):
        return request(BASE_URLS['reload'] % self.subdomain, {},
                       headers={
                           'Cookie': 'web_session_id=%s' % self.session_id
                       },
                       method='GET')
