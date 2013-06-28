#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.api import memcache
from APIs.api_keys import GMAP_API_KEY, VK_APP_KEY, VK_APP_SECRET, VK_AUTH_REDIRECT_URI
import logging
import webapp2
import handler
import model
import json


class Home(handler.Base):
    def get(self):
        self.render('home.html', vk_key=VK_APP_KEY, vk_secret=VK_APP_SECRET, vk_redirect_url=VK_AUTH_REDIRECT_URI)

class Map(handler.Base):
    def get(self):
        self.request.headers['Content-Type'] = 'text/plain'
        self.uid = self.request.cookies.get('uid')  # get uid(key) from cookie
        user = model.User.get_by_id(self.uid)
        address, coord = self.location(user)
        self.render('map.html', user=user, address=address, location=coord, gmap_key=GMAP_API_KEY)

    def friends_to_json(self, friends):
        friends_no_json = []
        for friend in friends:
          #  if len(friends_no_json) < 500:
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


class Json(Map):
    def get(self):
        self.request.headers['Content-Type'] = 'text/plain'
        self.uid = self.request.cookies.get('uid')  # get uid(key) from cookie
        friends = memcache.get('%s friends' % self.uid)
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
