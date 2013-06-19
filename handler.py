#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Base handler, used in most of handlers.
"""

import webapp2
from webapp2_extras import jinja2
from webapp2_extras import sessions


class Base(webapp2.RequestHandler):
  """ The other handlers inherit from this class. Provides some helper methods
for rendering a template.

The webapp2.cached_property decorator does two things:
1. Caches the value after the first time the property is accessed (rather than
recalculate it each time). Our session store and session aren’t going to
change in the course of the request, so it will speed things up to cache them.
2. Converts the method into a property like using the builtin @property
decorator so you can access it like self.session['some_var'] rather than
self.session()['some_var'].
"""

  def dispatch(self):
    """ One of the advantadges of webapp2 over webapp is that you can wrap the
dispatching process of webapp2.RequestHandler to perform actions before
and/or after the requested method is dispatched. You can do this overriding
the webapp2.RequestHandler.dispatch() method. This can be useful, for
example, to test if requirements were met before actually dispatching the
requested method, or to perform actions in the response object after the
method was dispatched.
"""

    try:
      # Dispatch the request.
      webapp2.RequestHandler.dispatch(self)
    finally:
      # Save all sessions.
      self.session_store.save_sessions(self.response)

  @webapp2.cached_property
  def session_store(self):
    return sessions.get_store(request=self.request)

  @webapp2.cached_property
  def session(self):
    """ Returns a session using the default cookie key.
"""
    return self.session_store.get_session(backend='securecookie')

  def jinja2_factory(self, app):
    """ True ninja method for attaching additional globals or filters to jinja2.
"""
    j = jinja2.Jinja2(app)
    j.environment.filters.update({
    })
    j.environment.globals.update({
      'uri': webapp2.uri_for,
    })
    return j

  @webapp2.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(factory=self.jinja2_factory)

  def render(self, _template, **context):
    rv = self.jinja2.render_template(_template, **context)
    self.response.write(rv)