#new AVR

from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators

app = Flask(__name__)

@app.route('/')

def index():

	return render_template('testform.html')


	
if __name__ == '__main__':
	app.run(debug=True)