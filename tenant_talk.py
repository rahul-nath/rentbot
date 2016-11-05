import os
import webapp2
import jinja2
from google.appengine.ext import ndb

from pb_py import main as pbApi
host = 'aiaas.pandorabots.com'

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

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class StudentPage(Handler):
	def get(self):
		self.render('student.html', questions=questions)

	def post(self):
		content = self.request.get("question")
		API.talk(user_key, app_id, host, botname, input_text, session_id, recent=True)
		self.redirect('/results?question=' + content)

app = webapp2.WSGIApplication([('/', StudentPage),], debug=True)
