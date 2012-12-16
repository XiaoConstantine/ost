#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import webapp2 
from google.appengine.api import users
from google.appengine.ext import webapp
#from google.appengine.ext.webapp.util import run_wsgi_app

#import django

#class MainPage(webapp2.RequestHandler):
#	def get(self):
		
#   		if users.get_current_user():
#			url = users.create_logout_url(self.request.uri)
#			url_linktext = 'Logout'
#		else:
#			url = users.create_login_url(self.request.uri)
#			url_linktext = 'Login'
#
#		template_values = {
			#'greetings': greetings,
#			'url': url,
#			'url_linktext': url_linktext,
#		}

#		path = os.path.join(os.path.dirname(__file__), 'html/log.html')
#		self.response.out.write(template.render(path, template_values))
#app = webapp2.WSGIApplication([('/', MainPage)], debug = True)

class MainPage(webapp2.RequestHandler):  
	def get(self):  
		self.response.out.write(""" 
			<html> 
			 <body> 
				<form action="/sign" method="post"> 
				<div><textarea name="content" rows="3" cols="60"></textarea></div> 
				<div><input type="submit" value="Sign Guestbook"></div> 
			</form> 
			</body> 
			</html>""")  
  
class Guestbook(webapp2.RequestHandler):  
	def post(self):  
		self.response.out.write('<html><body>You wrote:<pre>')  
		self.response.out.write(cgi.escape(self.request.get('content')))  
		self.response.out.write('</pre></body></html>')  
  
app = webapp2.WSGIApplication([('/', MainPage),('/sign', Guestbook)],debug=True)  
  
#def main():  
#	run_wsgi_app(application)  
  
#if __name__ == "__main__":  
#	main()  
