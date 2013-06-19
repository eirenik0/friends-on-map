#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import urllib

from google.appengine.api import urlfetch

import handler
import model


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

    self.response.out.write(uid)

    #user_info = urlfetch.fetch(url='https://api.vk.com/method/users.get?uids=%s&fields=uid,first_name,last_name,city,country,photo_rec&access_token=%s' % (uid, token),
    # method=urlfetch.POST).content
    
    #user_info = json.loads(user_info)
    
    #city = urlfetch.fetch(url='https://api.vk.com/method/getCities?cids=665&access_token=%s' % token, method=urlfetch.POST).content
    
    #country = urlfetch.fetch(url='https://api.vk.com/method/getCountries?cids=1,2,3,4,5&access_token=%s' % token, method=urlfetch.POST).content
 
    #return self.redirect('/')