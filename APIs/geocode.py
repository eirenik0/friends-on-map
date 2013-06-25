__author__ = 'infernion'
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'infernion'

from google.appengine.api import memcache
from google.appengine.api import urlfetch
import json


class Geocode(object):

    def get(self, address):
        format_address = "+".join(address.split())
        #print format_adress
        cached_location = memcache.get('%s' % format_address)
        if cached_location is not None:
            return cached_location
        else:
            geodata_json = urlfetch.fetch(
                        url="https://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % format_address,
                        method=urlfetch.POST).content
            geodata = json.loads(geodata_json)
            try:
                geodata = geodata['results'][0]['geometry']['viewport']['northeast']
                location = [geodata['lat'], geodata['lng']]
                memcache.add('%s' % format_address, location)
            except IndexError:
                return [-82.471829, -118.857425]

