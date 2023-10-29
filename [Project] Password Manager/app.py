from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import json
import os

# SQL configuration.
app = Flask(__name__)
app.secret_key = "sikret_pass"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
JSON_FILE = "users.json"

# Create SQLAlchemy table.
class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.password}')"

# Create new database.
with app.app_context():
    db.create_all()

# Read and write JSON.
def read_users():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    return {}

def write_users(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file)

# Routes for different functions.
@app.route('/')
def index():
    return render_template("log-in.html")

@app.route('/log', methods=['POST'])
def log():
    user_id = request.form.get("user-id")
    password = request.form.get("password")
    users = read_users()
    passwords = Password.query.all()

    if user_id in users:
        if users[user_id] == password:
            return render_template("view-pw.html", passwords=passwords)
        else:
            flash("Wrong password!")
            return redirect(url_for('index'))
    elif users:
        flash("User ID does not exist!")
        return redirect(url_for('index'))
    else:
        users[user_id] = password
        write_users(users)
        flash("User ID and Password have been registered!")
        return redirect(url_for('index'))

@app.route('/addpassword', methods=['POST'])
def addpassword():
    password_name = request.form['passwordName']
    password_value = request.form['passwordValue']

    # Create a new password entry
    new_password = Password(name=password_name, password=password_value)

    # Add the new password to the database
    db.session.add(new_password)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/filter', methods=['POST'])
def filter():
    filter = request.form.get('filter')

    filters = []

    if filter:
        password_filter = (Password.name.like(f"%{filter}%"))
        filters.append(password_filter)

    results = Password.query.filter(*filters).all()
    return render_template('view-pw.html', results=results)

@app.route('/allpassword', methods=['GET'])
def show_all_passwords():
    all_passwords = Password.query.all()
    return render_template('view-pw.html', results=all_passwords)

if __name__ == '__main__':
    app.run(debug=True)