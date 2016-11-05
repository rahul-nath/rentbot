import os
import webapp2
import jinja2
from google.appengine.ext import ndb

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


hangouts = []

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape = True)

def question_key(question):
  return ndb.Key("Question", question)

def hangouts_key(hangout):
  return ndb.Key("Hangout", hangout)



class Question(ndb.Model):
	content = ndb.StringProperty(indexed=False)
	hangout = ndb.StringProperty(indexed=False)
	student_count = ndb.IntegerProperty(indexed=False)

class Hangout(ndb.Model):
	hangout = ndb.StringProperty(indexed=False)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
			self.write(self.render_str(template, **kw))

class LoginPage(Handler):
	def get(self):
		# if the Datastore is empty,
		# put all the hangouts in the Datastore
		hangouts_query = Hangout.query(ancestor=hangouts_key("Hangout"))
		exists = hangouts_query.count(limit=1)
		if not exists:
			for h in hangouts:
				session = Hangout(parent=hangouts_key("Hangout"))
				session.hangout = h
				session.put()
		self.render('index.html')

# TODO call question.put() if they click the button on the redirect page
# that says "question not on here." If this doesn't work, need to change
class StudentPage(Handler):
	def get(self):
		questions_query = Question.query(ancestor=question_key("Question"))
		questions = questions_query.fetch()
		print questions
		self.render('student.html', questions=questions)

	def post(self):
		content = self.request.get("question")
		self.redirect('/results?question=' + content)

class TutorPage(Handler):
	def get(self):
		# query for asked questions
		questions_query = Question.query(ancestor=question_key("Question"))
		questions = questions_query.fetch()
		self.render('tutor.html', questions=questions)


# TODO: Delete the hangout object from the Datastore
# TODO: When the service is over, or 24 hours is up, clear the Datastore
# 		and return the hangout links to the datastore
class ResultsPage(Handler):
	def get(self):
		content = self.request.get("question")
		questions_query = Question.query(ancestor=question_key("Question"))
		questions = questions_query.fetch()
		self.render('results.html', questions=questions, content=content)

	def post(self):
		content = self.request.get("content")

		hangouts_query = Hangout.query(ancestor=hangouts_key("Hangout"))
		session = hangouts_query.fetch(1)[0]

		question = Question(parent=question_key("Question"))
		question.content = content
		question.hangout = session.hangout
		question.student_count = 1
		question.put()

		# is this the right way to delete from the Datastore?`
		print session
		session.key.delete()
		self.redirect(str(question.hangout))


app = webapp2.WSGIApplication([('/', LoginPage),
								('/tutor', TutorPage),
								('/student', StudentPage),
								('/results', ResultsPage),],
								debug=True)
