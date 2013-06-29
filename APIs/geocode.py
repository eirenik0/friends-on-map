#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'infernion'

from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
from google.appengine.ext import ndb
import json
import time
import model


class Geocode(object):
    def get(self, address):
        """
        For convert address string to list geo data
        :type self: object
        :param address: like "city, country"
        :return: geodata [lat, lng]
        """
        format_address = "+".join(address.split())
        cached_coords = memcache.get('%s' % format_address)
        if cached_coords is not None:
            return cached_coords
        else:
            geodata = {u'status': u'', u'results': []}
            while not geodata['results']:
                geodata_json = urlfetch.fetch(
                            url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % format_address,
                            method=urlfetch.POST).content
                geodata = json.loads(geodata_json)
                time.sleep(1)
            print geodata
            try:
                geodata = geodata['results'][0]['geometry']['viewport']['northeast']
                coords = [geodata['lat'], geodata['lng']]
                memcache.add('%s' % format_address, coords) # add new location to memcache
                self.write_db(format_address, coords)
                return coords
            except IndexError:
                return [-82.471829, -118.857425]

    def write_db(self, address, coords):
        location = model.CityLocation()
        location.populate(address=address,
                          coords=coords)
        location.key = ndb.Key(model.CityLocation, location.address)
        location.put()

    def do_transaction(self):
        taskqueue.add(url='/map', transactional=True)
