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
import random
import webapp2 
from google.appengine.api import users
from google.appengine.ext import webapp
import os
import django
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from xml.dom import minidom

#from upload.models import Upload


#-----class definition------#
# Basic class we need:      #
#                           #
#-----Category--------------#
#-----Item------------------#
class Category(db.Model):
	name = db.StringProperty()
	user = db.UserProperty()
	
class Item(db.Model):
    name = db.StringProperty()
    wins = db.IntegerProperty(default=0)
    loses = db.IntegerProperty(default=0)
    category  = db.ReferenceProperty(Category, collection_name='items')


#############################################################
#Handlers
#############################################################


#Login Page Handler
class MainPage(webapp2.RequestHandler):
	def get(self):
   		user = users.get_current_user()
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': user, 
			'url': url,
			'url_linktext': url_linktext,
		}

		path = os.path.join(os.path.dirname(__file__), 'html/log.html')
		self.response.out.write(template.render(path, template_values))

#Vote Button Handler
class Vote(webapp2.RequestHandler):  
	def post(self):
		user = users.get_current_user()
		categorys = db.GqlQuery("SELECT * FROM Category")
		template_values = {
				'user': user,
				'categorys': categorys,
				}
		path = os.path.join(os.path.dirname(__file__), 'html/vote.html')
		self.response.out.write(template.render(path, template_values)) 

#Add Category Handler
class addCategory(webapp2.RequestHandler):  
	def post(self):
		user = users.get_current_user()
		old_categorys = Category(name='', user=users.get_current_user())
		old_categorys = db.GqlQuery("SELECT * FROM Category")
		add_category = Category(name='', user = users.get_current_user())
		url = '/'
		url_linktext = 'Back to Log'
	
		add_category.name = self.request.get('add_Category')

		add_category.put()
	
		template_values = {
				'user': user,
				'old_categorys': old_categorys,
				'category': add_category,
				'url': url,
				'url_linktext': url_linktext,
				}
		path = os.path.join(os.path.dirname(__file__), 'html/addCategory.html')
		self.response.out.write(template.render(path, template_values))  

#Choose one category to add items
class chooseCategoryToAdd(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()
		categorys = db.GqlQuery("SELECT * FROM Category")
		url = '/'
		url_linktext = 'Back to log'
		template_values = {
				'user': user,
				'categorys': categorys,
				'url': url,
				'url_linktext': url_linktext,
				}
		path = os.path.join(os.path.dirname(__file__), 'html/chooseCategoryToAdd.html')
		self.response.out.write(template.render(path, template_values))


#Add new Item to category
#Search specific category by category_key
#then put the new item into category
class addItem(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()
		category = Category(name='', user=users.get_current_user())
		url = '/'
		url_linktext = 'Back to log'
		
		category_key = self.request.get("category_key")
		category = db.get(category_key)
		item = Item()
		item.name = self.request.get('item')
		item.category = category
		item.put()
		template_values = {
                'category': category,
				'user': user,
				'old_item': category.items,
				'item': item,
				'url': url,
				'url_linktext': url_linktext,
				}
		path = os.path.join(os.path.dirname(__file__), 'html/addItem.html')
		self.response.out.write(template.render(path, template_values))

#Show Result Handler
class Result(webapp2.RequestHandler):
    def post(self):
        url = '/'
        url_linktext = 'Back to Log'
        user = users.get_current_user()
        item = users.get_current_user()
        category_key = self.request.get("category_key")
        category = db.get(category_key)
        
        template_values = {
            'user': user,
            'category': category,
            'items':category.items,
            'url': url,
            'url_linktext': url_linktext,
        }
        path = os.path.join(os.path.dirname(__file__),'html/result.html')
        self.response.out.write(template.render(path,template_values))

#Vote Handler
class voteItem(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()
		category_key = self.request.get("category_key")
		category = db.get(category_key)
		randomList = []
		items = list(category.items)
		
		for item in items:
			if item.name:
				randomList.append(item)

        
		length = len(randomList)
		firstIndex = random.randint(0,length-1)
		secondIndex = random.randint(0, length-1)
		while(firstIndex==secondIndex):
			secondIndex = random.randint(0,length-1)

		firstItem = randomList[firstIndex]
		secondItem = randomList[secondIndex]
		template_values = {
				'user': user,
				'category': category,
				'firstItem':  firstItem,
				'secondItem': secondItem,
				}
		path = os.path.join(os.path.dirname(__file__), 'html/vote_item.html')
		self.response.out.write(template.render(path, template_values))

#Vote Result Handler
class RecordVote(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        category_key = self.request.get("category_key")
        category = db.get(category_key)
        items_list = list(category.items)
        randomlist =[]
        for item in items_list:
            if item.name:
                randomlist.append(item)
        count=len(randomlist)
        firstIndex = random.randint(0,count-1)
        secondIndex = random.randint(0,count-1)
        while (firstIndex == secondIndex):
            secondIndex = random.randint(0,count-1)
        firstItem = randomlist[firstIndex]
        secondItem = randomlist[secondIndex]
    
        items = self.request.get("win_lose")
        items = items.split('/')
        itemWin = Item()
        itemLose = Item()
        for item in randomlist:
            if (item.name == items[0]):
                item.wins += 1
                itemWin = item
            elif (item.name == items[1]):
                item.loses += 1
                itemLose = item
        
        itemWin.put()
        itemLose.put()
        
        template_values = {
            'user': user,
            'category': category,
            'itemWin': itemWin,
            'itemLose': itemLose,
            'firstItem': firstItem,
            'secondItem': secondItem,
        }
        path = os.path.join(os.path.dirname(__file__),'html/recordVoteResult.html')
        self.response.out.write(template.render(path,template_values))

#Handler which for user to choose one category to check the final results
class ChooseCategoryToResult(webapp2.RequestHandler):
    def post(self):
        categorys = Category(name="",
                             user=users.get_current_user())
        categorys = db.GqlQuery("SELECT * FROM Category")
        template_values = {
            'categorys': categorys
        }
        path = os.path.join(os.path.dirname(__file__),'html/chooseCategoryToResult.html')
        self.response.out.write(template.render(path,template_values))

#class ExportToXML(webapp2.RequestHandler):
    
        



class ImportFromXML(webapp2.RequestHandler):
    def get(self):
        try:
            url = fetch()
            xml = parseString(url.content)
            self.response.out.write("<html><body><table>")
            self.response.out.write(outputHTML(xml))
            self.response.out.write("</table></body></html>")
        except(TypeError, ValueError):
            self.response.out.write("<html><body><p>Invalid</p></body></html>")


    def post(self):
        user = users.get_current_user()
        url = '/'
        url_linktext = 'Back to Log'
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext
        }
        path = os.path.join(os.path.dirname(__file__), 'html/ImportFromXML.html')
        self.response.out.write(template.render(path,template_values))

            
######################################################################





app = webapp2.WSGIApplication([('/', MainPage),
								('/Vote', Vote),
								('/result',Result),
								('/addCategory', addCategory),
								('/chooseCategoryToAdd', chooseCategoryToAdd),
                                ('/ChooseCategoryToResult',  ChooseCategoryToResult),
                                ('/ImportFromXML', ImportFromXML),
                                ('/RecordVote', RecordVote),
								('/addItem', addItem),
								('/voteItem', voteItem)],debug=True)  


#if __name__=="__main__":
#	main()
#def main():  
#	run_wsgi_app(application)  
  
#if __name__ == "__main__":  
#	main()  
