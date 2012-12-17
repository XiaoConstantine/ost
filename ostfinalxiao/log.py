#!usr/bin/python
from google.appengine.api import users
from google.appengine.ext import webapp
import wsgiref.handlers
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import datetime

from google.appengine.dis import use_library
use_library('django','1.4')

##############Models####################
#class category(db.Model):
#      item = db.StringProperty();
#
#

class Polls(db.Model):
	category = db.UserProperty()
    item = db.StringProperty()

	users = db.StringListProperty()
	create_time = db.DateTimeProperty()

class vote(db.Model):

