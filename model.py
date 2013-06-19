#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from webapp2_extras.appengine.auth.models import User


class User(User):
  """ Stores user info.
Expending existing webapp2 user object.
"""
  uid = ndb.IntegerProperty()
  name = ndb.StringProperty(indexed=False)
  city = ndb.StringProperty(indexed=True)
  followers = ndb.JsonProperty()
  followers_count = ndb.IntegerProperty(indexed=False)
  photo = ndb.StringProperty()

key = ndb.Key
