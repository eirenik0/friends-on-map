#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib

from google.appengine.api import urlfetch

import handler
from model import User


KEY = '3720247'
SECRET = 'uOmPND7Xogaafizp6Xah'
REDIRECT_URI = r'http://friends-on-map.appspot.com/auth/vk'


class Auth(handler.Base):
  """ Auth handler.

Args:
code: Get var with auth code from vk.

Returns:
Auths user and redirects him to home page.
"""
  def get(self):
    code = self.request.get('code')
    payload = urllib.urlencode({
      'redirect_uri': REDIRECT_URI,
      'client_secret': SECRET,
      'code': code,
      'client_id': KEY})
    token = urlfetch.fetch(
        url='https://oauth.vk.com/access_token?%s' % payload,
        method=urlfetch.GET).content
    token_json = json.loads(token)
    token = token_json['access_token']
    uid = token_json['user_id']
    user_info_json = urlfetch.fetch(
        url='https://api.vk.com/method/users.get?uid=%s&fields=uid,first_name,last_name,city,country,photo_rec&access_token=%s' % (uid, token),
        method=urlfetch.POST).content
    user_info = json.loads(user_info_json)
    user_info = user_info['response'][0]

    name, countryid, cityid, photo_url = ('%s %s' % (user_info['first_name'], user_info['last_name']),
                                          user_info['country'],
                                          user_info['city'],
                                          user_info['photo_rec'])

    country_json = urlfetch.fetch(
        url='https://api.vk.com/method/places.getCountryById?cids=%s&access_token=%s' % (countryid, token),
        method=urlfetch.POST).content
    country = country_json['response'][0]['name']

    city_json = urlfetch.fetch(
        url='https://api.vk.com/method/places.getCityById?cids=%s&access_token=%s' % (cityid, token),
        method=urlfetch.POST).content
    city = city_json['response'][0]['name']

    self.response.out.write(name, country, city, photo_url)
