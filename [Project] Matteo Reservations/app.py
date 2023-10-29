from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
from flask_migrate import Migrate
from datetime import datetime, date
from sqlalchemy import and_
from flask import request, jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///matteoreservation.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class YourTable(db.Model):
    __tablename__ = 'matteores'
    index = db.Column(db.Integer, primary_key=True)
    table_class = db.Column(db.String)
    id = db.Column(db.Integer, db.CheckConstraint('LENGTH(CAST(id AS TEXT)) = 6'), nullable=False)
    surname = db.Column(db.String, nullable=False)
    dateofres = db.Column(db.Date, nullable=False)
    time_start = db.Column(db.Time, nullable=False)
    time_end = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id

# Create the table inside the application context
with app.app_context():
    db.create_all()

def get_valid_table_classes():
    valid_table_classes = []
    current_time = datetime.now().time()

    with app.app_context():
        rows = YourTable.query.all()
        for row in rows:
            if row.dateofres == date.today():
                if row.time_start <= current_time <= row.time_end:
                    valid_table_classes.append(row.table_class)

    return valid_table_classes

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    # Retrieve form data
    table_class = str(request.form['table_class_input'])
    id = request.form['id']
    surname = request.form['surname']
    dateofres_str = request.form['dateofres']  # Get date string from form
    time_start_str = request.form['time_start']  # Get time string from form
    time_end_str = request.form['time_end']  # Get time string from form

  # Check if any required fields are empty
    if not all([table_class, id, surname, dateofres_str, time_start_str, time_end_str]):
        return render_template('input-invalid.html')

    # Convert date and time strings to Python date and time objects
    # Convert date and time strings to Python date and time objects
    try:
        dateofres = datetime.strptime(dateofres_str, '%Y-%m-%d').date()
        time_start = datetime.strptime(time_start_str, '%H:%M').time()
        time_end = datetime.strptime(time_end_str, '%H:%M').time()
    except ValueError:
        return render_template('input-invalid.html')


    if len(id) != 6:
        return render_template('input-invalid.html')
    
    if time_end <= time_start:
        return render_template('input-invalid.html')

    # Check if there is an existing reservation with the same date, time period, and table class
    with app.app_context():
        existing_reservation = YourTable.query.filter(and_(
            YourTable.table_class == table_class,
            YourTable.dateofres == dateofres,
            YourTable.time_start <= time_end,
            YourTable.time_end >= time_start
        )).first()

        if existing_reservation:
            return render_template('double-booked.html')

        # Create the scoped_session inside the application context
        db_session = scoped_session(sessionmaker(bind=db.engine))

        # Insert data into the table using SQLAlchemy
        new_record = YourTable(
            table_class=table_class,
            id=id,
            surname=surname,
            dateofres=dateofres,
            time_start=time_start,
            time_end=time_end
        )

        # Use the scoped_session to add and commit the record
        db_session.add(new_record)
        db_session.commit()

        # Close the session to release resources
        db_session.close()

    # Provide feedback to the user
    return render_template('reserve-submitted.html')

@app.route('/', methods =['GET', 'POST'])
def index():
    return render_template('welcome-page.html')

@app.route('/welcomepage', methods =['GET', 'POST'])
def welcomepage():
    return render_template('welcome-page.html')

@app.route('/about', methods =['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/birdseye', methods =['GET', 'POST'])
def birdseye():
    return render_template('birds-eye.html')

@app.route('/templates/all-reservations.html', methods =['GET', 'POST'])
def all_reservations():
    reservations = YourTable.query.order_by(YourTable.dateofres).all()
    return render_template('all-reservations.html', reservations=reservations)

@app.route('/templates/cancel-reservation.html', methods =['GET', 'POST'])
def cancel_reservation():
    return render_template('cancel-reservation.html')

@app.route('/templates/my-reservations.html', methods = ['POST', 'GET'])
def my_reservations():
    if request.method == 'POST':
        username = request.form['username']
            # Create an application context to use the db_session
        try:
            user_id = int(username)
            if len(username)!=6:
                return render_template('wrong-id.html')
        except ValueError:
            # Handle the case where the username is not a valid integer
            return render_template('wrong-id.html')

        with app.app_context():
            # Create the scoped_session inside the application context
            db_session = scoped_session(sessionmaker(bind=db.engine))

            # Filter the records based on the username
            tasks = db_session.query(YourTable).filter_by(id=user_id).order_by(YourTable.dateofres).all()

            # Close the session to release resources
            db_session.close()

            return render_template('my-reservations.html', tasks=tasks)
    else:
        return render_template('welcome-page.html')

@app.route('/delete/<int:index>')
def delete(index):
    task_to_delete = YourTable.query.get_or_404(index)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return render_template('welcome-page-2.html')
    except:
        return render_template('cancel-reservation-fail.html') 

@app.route('/templates/double-booked.html', methods =['GET', 'POST'])
def double_booked():
    return render_template('double-booked.html')

@app.route('/templates/input.html', methods =['GET', 'POST'])
def input():
    return render_template('input.html')

@app.route('/templates/room-c.html', methods =['GET', 'POST'])
def room_c():
    valid_table_classes = get_valid_table_classes()
    return render_template('room-c.html', valid_table_classes=valid_table_classes)

@app.route('/templates/room-d.html', methods =['GET', 'POST'])
def room_d():
    valid_table_classes = get_valid_table_classes()
    return render_template('room-d.html', valid_table_classes=valid_table_classes)

@app.route('/templates/reserve-submitted.html')
def success():
    return render_template('reserve-submitted.html')

@app.route('/templates/welcome-page-2.html')
def welcome_page_2():
    return render_template('welcome-page-2.html')

if __name__ == '__main__':
    app.run(debug = True, port = 8080)