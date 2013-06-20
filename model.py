#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb


class User(ndb.Model):
  """ Stores user info.
Expending existing webapp2 user object.
"""
  uid = ndb.StringProperty()
  name = ndb.StringProperty()
  city = ndb.StringProperty()
  country = ndb.StringProperty()
  friends = ndb.JsonProperty()
  photo = ndb.StringProperty()

