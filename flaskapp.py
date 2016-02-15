import os
from datetime import datetime

import re
from flask import Flask, request, flash, url_for, redirect, \
     render_template, abort, send_from_directory, json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Documents/Skola/TDDD83/formAnwers.db'
db = SQLAlchemy(app)


class formAnswers(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(80), unique=True)
    message = db.Column(db.String(120), unique=False)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name



@app.route('/')
def index():
   return render_template('index.html')

def is_email_address_valid(InputEmail):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", InputEmail):
        return False
    return True

@app.route('/contact', methods=['GET','POST'])
def contact():
    errors=''
    if request.method == "GET": # If the request is GET, render the form template.
        return render_template("contact.html", errors=errors)
    else:
        InputName = request.form['InputName'].strip()
        InputEmail = request.form['InputEmail'].strip()
        InputMessage = request.form['InputMessage'].strip()
        if not InputName or not InputEmail or not InputMessage:
            errors = "Please enter all the fields."
        if not errors:
            if not is_email_address_valid(InputEmail):
                errors = errors + "Please enter a valid email address"
        if not errors:
            print(InputName, InputMessage, InputEmail)
            return "Dina data laddades in korrekt"
        if errors:
            return errors
        return render_template('/contact', errors=errors)



@app.route('/bocker')
def bocker():
    return render_template('bocker.html')

@app.route('/om')
def om():
    return render_template('om.html')


@app.route('/<path:resource>')
def serveStaticResource(resource):
    return send_from_directory('static/', resource)

@app.route("/test")
def test():
    return "<strong>It's Alive!</strong>"

if __name__ == '__main__':
    app.run()
