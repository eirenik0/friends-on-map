#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'infernion'

from google.appengine.api import memcache
from APIs.api_keys import GMAP_API_KEY, VK_APP_KEY, VK_APP_SECRET, VK_AUTH_REDIRECT_URI
from APIs.geocode import Geocode
from APIs.vk import UserData
import logging
import webapp2
import handler
import model
import json
import time


class Home(handler.Base):
    def get(self):
        self.render('home.html', vk_key=VK_APP_KEY, vk_secret=VK_APP_SECRET, vk_redirect_url=VK_AUTH_REDIRECT_URI)


class Map(handler.Base):
    def get(self):
        self.request.headers['Content-Type'] = 'text/plain'
        uid = self.request.cookies.get('uid')  # get uid(key) from cookie
        user = model.User.get_by_id(uid)
        address = '%s, %s' % (user.country, user.city)
        geo = Geocode().get(address)
        coords = "%s, %s" % (geo[0], geo[1])
        Map.user = user
        self.render('map.html', user=user, address=address, location=coords, gmap_key=GMAP_API_KEY)


class Json(handler.Base):
    def get(self):
        user = Map.user
        friends = user.friends
        friends_json = self.friends_to_json(friends)
        self.write(friends_json)

    def friends_to_json(self, friends):
        friends_no_json = []
        for friend in friends:
            try:
                friends_no_json.append({'lat': friend['location'][0],
                                        'lng': friend['location'][1],
                                        'name': friend['name'],
                                        'address': friend['address'],
                                        'url': "https://vk.com/%s" % friend['uid'],
                                        'photo': friend['photo']})
            except:
                pass
        friends_json = json.dumps(friends_no_json)
        return friends_json


class Load(handler.Base):
    def get(self):
        self.render('load.html')


config = {'webapp2_extras.sessions': {
    'secret_key': 'LKsdt4223o5khsdt9',
    'session_max_age': None,
    'cookie_args': {
        'max_age': 31556926,
        'domain': None,
        'path': '/',
        'secure': None,
        'httponly': True,
    },
}}

logging.getLogger().setLevel(logging.DEBUG)
application = webapp2.WSGIApplication([
    (r'/', Home),
    (r'/auth/vk', 'APIs.vk.Auth'),
    (r'/map', Map),
    (r'/json', Json),
    (r'/load', Load),
    (r'/data', 'APIs.vk.UserData'),

], debug=True, config=config)
