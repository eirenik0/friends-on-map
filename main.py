#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import webapp2
import handler
import model
from APIs.vk import KEY, SECRET


class Home(handler.Base):
    def get(self):
        self.render('home.html', key=KEY, secret=SECRET)


class Map(handler.Base):
    def get(self):
        user = model.User()
        self.render('map.html', user=user)

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'LKsdt4223o5khsdt9',
    'session_max_age': None,
    'cookie_args': {
        'max_age': 31556926,
        'domain': None,
        'path': '/',
        'secure': None,
        'httponly': True,
    },
}

logging.getLogger().setLevel(logging.DEBUG)
application = webapp2.WSGIApplication([
    (r'/', Home),
    (r'/auth/vk', 'APIs.vk.Auth'),
    (r'/map', Map)


], debug=True, config=config)
