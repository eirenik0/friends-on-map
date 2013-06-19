#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import webapp2
import handler
from APIs.vk import KEY, SECRET

class Home(handler.Base):
  def get(self):
    self.render('home.html', key=KEY, secret=SECRET)


class Logout(handler.Base):
  def get(self):
    self.session['user_id'] = None
    return self.redirect('/')


config = {}
config['webapp2_extras.sessions'] = {
  'secret_key': 'MY SUPER SECRET COOKIE KEY FOR VK APPLICATION!!!11',
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
  (r'/auth/vk', 'vk.Auth'),
  (r'/logout', Logout),

], debug=True, config=config)
