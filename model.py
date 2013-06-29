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
    photo = ndb.StringProperty()
    token = ndb.StringProperty()
    friends = ndb.PickleProperty(repeated=True)








