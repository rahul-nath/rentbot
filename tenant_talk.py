import os
import webapp2
import jinja2
from google.appengine.ext import ndb

from PbPython import main as pbApi
host = 'aiaas.pandorabots.com'
from secret import app_id, user_key, botname

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
