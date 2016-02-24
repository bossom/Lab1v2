import re
from flask import Flask, request, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/testdb.db'
db = SQLAlchemy(app)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(80), unique=False)
    message = db.Column(db.String(120), unique=False)

    def __init__(self, name, email, message):
         self.name = name
         self.email = email
         self.message = message

    def __repr__(self):
         return '<form %r>' % self.name



@app.route('/')
def index():
   return render_template('index.html')

def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True

@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    errors = ''
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        message = request.form['message'].strip()
        if not name or not email or not message:
            errors = "Please enter all fields."
        if not errors:
            if not is_email_address_valid(email):
                errors = errors + "Please enter a valid email."
        if not errors:
            indata = {'name' : name,
                    'email' : email,
                    'message' : message,
                    }
            question = Question(name, email, message)
            db.session.add(question)
            db.session.commit()
            data = Question.query.all()
            print indata

            return render_template ('success.html', data=data)
        return render_template('contact.html', errors=errors)
    else:
        data = Question.query.all()
        return render_template('contact.html', data=data)



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
