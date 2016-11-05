import os
import webapp2
import jinja2
from google.appengine.ext import ndb

from pb_py import main as pbApi
host = 'aiaas.pandorabots.com'

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
		# TODO: get the questions from API
		questions = []
		self.render('student.html', questions=questions)

	def post(self):
		content = self.request.get("question")
		# TODO: get the questions from API
		API.talk(user_key, app_id, host, botname, input_text, session_id, recent=True)
		self.redirect('/?question=' + content)

app = webapp2.WSGIApplication([('/', StudentPage),], debug=True)
