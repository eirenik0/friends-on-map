#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import memcache
from APIs.vk import KEY, SECRET, REDIRECT_URI
import logging
import webapp2
import handler
import model
import json


class Home(handler.Base):
    def get(self):
        self.render('home.html', key=KEY, secret=SECRET, redirect_url=REDIRECT_URI)

class Map(handler.Base):
    def get(self):
        user = self.get_user_data('uid')
        address, coord = self.location(user)
        friends = memcache.get('friends')
        friends_json = self.friends_to_json(friends)
        self.render('map.html', name=user.name, photo=user.photo, address=address, location=coord, friends=friends,
                    friends_json=friends_json)

    def friends_to_json(self, friends):
        friends_no_json = []
        for friend in friends:
          #  if len(friends_no_json) < 500:
                try:
                    friends_no_json.append({'lat': friend['location'][0],
                                            'lng': friend['location'][1],
                                            'name': friend['name'],
                                            'address': friend['address']})
                except:
                    pass
        #print friends_no_json
        friends_json = json.dumps(friends_no_json)
        return friends_json

    def location(self, user):
        """
        :param user: user id(uid)
        :return: address from ndb, coordinates from IP
        """
        address = '%s, %s' % (user.country, user.city)
        coords = self.get_coords(self.request.remote_addr)  # receive location from id
        if coords == None:
            coords = "36.315125,-27.802738"
            return address, coords
        return address, coords

    def get_cookie(self, key):
        """
        :param key: key to find cookie
        :return: saved key value
        """
        self.request.headers['Content-Type'] = 'text/plain'
        cookie = self.request.cookies.get(key)  # get uid(key) from cookie
        return cookie

    def get_user_data(self, data):
        """
        :param data:
        :return: User class object from model
        """
        data_key = self.get_cookie(data)
        return model.User.get_by_id(data_key)


class Json(Map):
    def get(self):
        friends = memcache.get('friends')
        friends_json = self.friends_to_json(friends)
        self.write(friends_json)

class StaticMap(Map):
    def get(self):
        #uid = self.get_cookie('uid')
        #user = model.User.get_by_id(uid)
        #address, coord = self.location(user)
        self.render('map_static.html', photo='http://cs302810.vk.me/v302810263/40d5/NhHItwnqQxc.jpg',
                    address=u'Ukraine,Харьков')


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
    (r'/map', Map),
    (r'/map-static', StaticMap),
    (r'/json', Json),


], debug=True, config=config)
