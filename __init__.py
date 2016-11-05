from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
app = Flask(__name__)
app.secret_key = 'super_secret_key'

from pb_py import main as pbApi
host = 'aiaas.pandorabots.com'
from secret import app_id, user_key, botname
conversation = []
error = ''

@app.route('/', methods=['GET', 'POST'])
def showMain():
	'''Shows the main page'''
	if request.method == 'GET':
		return render_template('main.html', conversation=conversation, error=error)
	if request.method == 'POST':
		global error
		error = ''
		question = request.form.get('question', '')
		if question and not question.isspace():
			response = pbApi.talk(user_key, app_id, host, botname, question)
			answer = response['response'].replace('\n', '<br />')
			conversation.append((question, answer))
		else:
			error = 'Please enter a question'
		return redirect('/')

@app.route('/clear', methods=['POST'])
def clearHistory():
	'''Clears the chat history'''
	global conversation
	conversation = []
	return redirect('/')

if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)
