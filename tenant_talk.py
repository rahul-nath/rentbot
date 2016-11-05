import os
import webapp2
import jinja2
from google.appengine.ext import ndb

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
		# TODO: get questions from intermediary app

		self.render('student.html', questions=questions)

	def post(self):
		content = self.request.get("question")
		# TODO: send questions to chat api
		# TODO: get the answers from the chat api
		# this might mess up here
		self.redirect('?question=' + content)

class ResultsPage(Handler):
	def get(self):
		content = self.request.get("question")
		# TODO: get questions from intermediary app
		self.render('results.html', questions=questions, content=content)

	def post(self):
		content = self.request.get("content")

app = webapp2.WSGIApplication([('/', StudentPage),], debug=True)
