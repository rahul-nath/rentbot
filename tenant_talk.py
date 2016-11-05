import os
import webapp2
import jinja2
from google.appengine.ext import ndb

from pb_py import main as pbApi
host = 'aiaas.pandorabots.com'

from secret import app_id, user_key, botname

"""
	TODO:
	- create a post request in the student handler to add 1 to the student count
	- create a title summary input in the student facing side
	- sort frequency by title summary relevance; implement
	http://stevenloria.com/finding-important-words-in-a-document-using-tf-idf/
	- delete question, return the hangout after 30 minutes

	- create a small description for the question
	- directly pings the description of the problem to a slack channel -> decide on name

	- create an issue directly in slack and it gets put in the dashboard, with description
	- join the hangout from slack
	- delete the post in the slack channel and from the dashboard as soon as everyone leaves
		- figure out how to determine when no one is on a hangout
"""

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)
conversation = []

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		self.render('main.html', conversation=conversation)

	def post(self):
		question = self.request.get('question')
		response = pbApi.talk(user_key, app_id, host, botname, question)
		conversation.append((question, response['response']))
		self.render('main.html', conversation=conversation)

app = webapp2.WSGIApplication([('/', MainPage),], debug=True)
