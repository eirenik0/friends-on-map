#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from webapp2_extras.appengine.auth.models import User


class User(User):
  """ Stores user info.
Expending existing webapp2 user object.
"""

  name = ndb.StringProperty(indexed=False)


key = ndb.Key
Key = ndb.Key