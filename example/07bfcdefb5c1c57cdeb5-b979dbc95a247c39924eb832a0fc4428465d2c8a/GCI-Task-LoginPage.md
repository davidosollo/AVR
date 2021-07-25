# Login page using Python, Flask and sqlite3 DB #
### How-to guide
[(Task for GCI 2015-16)](https://codein.withgoogle.com/dashboard/task-instances/6211328603586560/?sp-page=1)
Year: 2015-16
This guide will show how to create a simple login page with Flask (a python microframework) and a sqlite3 database.

##### 1. Database Schema and Models
As we are creating a simple user login app we need to store 2 basic values in the database: the username and the password.
In order to build the database we need to define a schema:

schema.sql :
```sql
drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    username text not null,
    password text not null
);
```
This sql orders define the structure of our database. This set of orders also deletes or 'drops' previously created sql tables.

After defining the schema of the db we can now build it (on terminal):
```sqlite3 database.db < schema.sql```

Now we can define and develop the python methods to handle this database.

models.py :
```python
import sqlite3 as sql

def insertUser(username,password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username,password))
    con.commit()
    con.close()

def retrieveUsers():
	con = sql.connect("database.db")
	cur = con.cursor()
	cur.execute("SELECT username, password FROM users")
	users = cur.fetchall()
	con.close()
	return users
```
We'll later call these methods from main.py to handle the database.

##### 2. HTML Login Form (+css styling)
The html code used for this app can be found in index.html file (in this same git). It uses the Flask template engine to render the 'logged users' list. 
The html contains a simple html form with two text type inputs: username and password, and a submit type input (Login button).

##### 3. Flask App
Flask is a python microframework intended for the developement of web applications (server side). This application works with a single flask function/route/url (views for convention) which answers to two types of HTTP methods (GET, POST). If the HTTP request is GET, the app returns the HTML form. In the case of a POST request (created after the form submission) it returns the list of logged users.

main.py :
```python
from flask import Flask
from flask import render_template
from flask import request
import models as dbHandler

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
	if request.method=='POST':
   		username = request.form['username']
   		password = request.form['password']
   		dbHandler.insertUser(username, password)
   		users = dbHandler.retrieveUsers()
		return render_template('index.html', users=users)
   	else:
   		return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
```
This app makes database calls in order to insert new users and to return the logged users list requested by the POST method. The Database Handler (models.py) methods are called when main.py has to acces and/or modify the database: ```dbHandler.insertUser(username, password)``` , ```users = dbHandler.retrieveUsers()```.

Note: The host parameter can be changed to 127.0.0.1 (localhost) instead of 0.0.0.0 .

##### 4. All together: Testing and explaining data's flow

To run the Flask app (server) type into your terminal: ```python main.py```
Output :
```
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
Open your browser and visit 0.0.0.0:5000 (or 127.0.0.1:5000), the html will render and show up the login form. The terminal should prompt something like this:
```
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [20/Dec/2015 15:31:53] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [20/Dec/2015 15:31:53] "GET /static/main.css HTTP/1.1" 200 -
127.0.0.1 - - [20/Dec/2015 15:31:53] "GET /favicon.ico HTTP/1.1" 404 -
```
If you complete and submit the form, the results will be also reflected in the terminal (pay attention at the POST method):
```
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [20/Dec/2015 15:31:53] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [20/Dec/2015 15:31:53] "GET /static/main.css HTTP/1.1" 200 -
127.0.0.1 - - [20/Dec/2015 15:31:53] "GET /favicon.ico HTTP/1.1" 404 -
127.0.0.1 - - [20/Dec/2015 16:50:13] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [20/Dec/2015 16:50:14] "GET /static/main.css HTTP/1.1" 200 -
127.0.0.1 - - [20/Dec/2015 16:50:14] "GET /favicon.ico HTTP/1.1" 404 -
127.0.0.1 - - [20/Dec/2015 16:50:17] "POST / HTTP/1.1" 200 -
```
Now the webapp should also show the list of logged users.
(It works!)