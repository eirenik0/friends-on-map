#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'infernion'
from api_keys import VK_APP_KEY, VK_APP_SECRET, VK_AUTH_REDIRECT_URI
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from geocode import Geocode
import handler
import urllib
import json
import logging


class Auth(handler.Base):
    """
    Auth handler.

    Args:
    code: Get var with auth code from vk.

    Returns:
    Auths user and redirects him to map page.
    """

    def get(self):
        self.get_token()
        self.all_country = self.url_fetch(method="places.getCountryById",
                                          cids=",".join(map(str, range(236))))
        user_info = self.url_fetch(method="users.get",
                                   fields="uid,first_name,last_name,city,country,photo_rec")
        user_friends = self.url_fetch(method="friends.get",
                                      fields="uid,first_name,last_name,country,city,photo")

        name, country, city, photo_url = ('%s %s' % (user_info['first_name'], user_info['last_name']),
                                          self.get_country(user_info['country']),
                                          self.get_city(user_info['city']),
                                          user_info['photo_rec'])

        friends = self.get_friends_from_json(user_friends)
        self.response.set_cookie('uid', self.uid)
        memcache.add('%s friends' % self.uid, friends, time=10000)

        # write user data to db
        self.write_ndb(self.uid, name=name, city=city, country=country,
                       photo=photo_url, token=self.token)
        self.redirect('/map')



    def get_token(self):
        """
        Get user secret token to access VK API
        """
        code = self.request.get('code')
        payload = urllib.urlencode({
            'redirect_uri': VK_AUTH_REDIRECT_URI,
            'client_secret': VK_APP_SECRET,
            'code': code,
            'client_id': VK_APP_KEY})
        self.token = urlfetch.fetch(
            url='https://oauth.vk.com/access_token?%s' % payload,
            method=urlfetch.GET).content
        token_json = json.loads(self.token)
        self.token = token_json['access_token']
        self.uid = str(token_json['user_id'])

    def get_country(self, id):
        """
        Taked id and return format country string
        :param id: current city id
        :return: string name
        """
        try:
            return self.all_country[int(id)-1]['name']
        except IndexError:
            return ""

    def get_city(self, id):
        """
        Take id and return format city string
        """
       # print "ID", id
        city = memcache.get('cid: %s' % id)
        if city is not None:
            return city
        else:
            try:
                get_city = (self.url_fetch(method="places.getCityById",
                                    cids=id))['name']
            except:
                return ""
            city = memcache.add('cid: %s' % id, get_city)
            return get_city


    def url_fetch(self, cids="", method="", fields=""):
        """
        This method formed QUERY with accepted parameter to VK API
        :param cids: for show country/city with id
        :param method: what query we do
        :param fields: what fields we will get
        :return: dict
        """
        value_json = urlfetch.fetch(
            url='https://api.vk.com/method/%s?uid=%s&cids=%s&fields=%s&access_token=%s' % (
                method, self.uid, cids, fields, self.token),
            method=urlfetch.POST).content
       # print "json",  value_json
        if method == "friends.get" or method == "places.getCountryById":
            try:
                #print "friends, country ",(json.loads(value_json))['response']
                return (json.loads(value_json))['response']  # If use get method return all item in value
            except IndexError:
                return ""
        try:
                #print "else", (json.loads(value_json))['response'][0]
                return (json.loads(value_json))['response'][0]   # Else set first
        except IndexError:
            return ""

    def get_friends_from_json(self, user_friends):
        """
        Convert json values to namedtuple
        :user_friends: dict user friends
        :return: list of friends form: ['First_name Last_name', 'City, Country', city=bool, country=bool]
        """
        def format_address(field, city_id, country_id):
            city = self.get_city(field[city_id])
            country = self.get_country(field[country_id])
            address = '%s, %s' % (city, country)
            location = Geocode().get(address)
            return address, location

        def format(field, first_name, last_name):
            return '%s %s' % (field[first_name], field[last_name])

        friends = []
        for field in user_friends:
            if 'country' in field:
                if 'city' in field:
                    # Friends with city and country
                    friends.append({'name': format(field, 'first_name', 'last_name'),
                                    'address': format_address(field, 'city', 'country')[0],
                                    'location': format_address(field, 'city', 'country')[1],
                                    'uid': field['uid'], 'photo': field['photo'] })

                elif 'city' not in field:
                    friends.append({'name': (format(field, 'first_name', 'last_name')),
                                    'address': format_address(field, '', 'country')[0],
                                    'location': format_address(field, '', 'country')[1],
                                    'uid': field['uid'], 'photo': field['photo']})
            else:
            # Who haven't home
                friends.append({'name': (format(field, 'first_name', 'last_name')),
                                'address': 'Antarctica',
                                'location': '-82.471829,-118.857425',
                                'uid': field['uid'], 'photo': field['photo']})
        return friends

