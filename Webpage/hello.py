from flask import Flask, request, redirect, url_for, render_template, session, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import DataError
from flask_login import LoginManager



app = Flask(__name__)
app.secret_key = 'patoromimatotentoprojektstojizato'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ubuntu@localhost/project3'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Hall(db.Model):
   id = db.Column('id', db.Integer, primary_key = True)
   room_id = db.Column(db.REAL)
   floor_id = db.Column(db.Integer)
   temperature = db.Column(db.REAL)
   humidity = db.Column(db.REAL)
   light = db.Column(db.REAL)
   gpsx = db.Column(db.REAL)
   gpsy = db.Column(db.REAL)
   date_stamp = db.Column(db.Date)
   time_stamp = db.Column(db.Time)


   def __init__(self, room_id, floor_id, temperature, humidity, light, gpsx, gpsy, date_stamp, time_stamp):
      self.room_id = room_id
      self.floor_id = floor_id
      self.temperature = temperature
      self.humidity = humidity
      self.light = light
      self.gpsx = gpsx
      self.gpsy = gpsy
      self.date_stamp = date_stamp
      self.time_stamp = time_stamp

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

users = []
users.append(User(id=1, username='eaamvas', password='heslo'))
users.append(User(id=2, username='eaarozv', password='heslo'))
users.append(User(id=3, username='eaapab', password='heslo'))
users.append(User(id=4, username='teacher', password='password'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        try:
            user = [x for x in users if x.username == username][0]
            if user and user.password == password:
                session['user_id'] = user.id
                return redirect(url_for('welcome'))
        except IndexError:
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/showdata', methods=["POST", "GET"])
def showdata():
    if not g.user:
        return redirect(url_for('login'))
    try:
        if request.method == "POST":
                user = request.form["nm"]
                mHall = Hall.query.filter((Hall.date_stamp == user))
                return render_template('hello.html', myHall=mHall, user = user)
        else:
            myHall = Hall.query.order_by(Hall.id.desc()).limit(144)
            return render_template('hello.html', myHall=myHall)
    except DataError:
        return render_template('hello.html', title='WRONG DATE')

    
@app.route('/main_hall')
def bye():
    if not g.user:
        return redirect(url_for('login'))
    myHall = Hall.query.order_by(Hall.id.desc()).limit(1)
    return render_template('main_hall.html', myHall=myHall)

@app.route('/')
def welcome():
    if not g.user:
        return redirect(url_for('login'))

    myHall = Hall.query.order_by(Hall.id.desc()).limit(1)
    return render_template('main.html', myHall=myHall)

@app.route('/all_rooms')
def all():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('all_rooms.html')

@app.route('/contact')
def contact():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('contact.html')

@app.route('/map')
def map():
    if not g.user:
        return redirect(url_for('login'))
    myHall = Hall.query.order_by(Hall.id.desc()).limit(1)
    return render_template('map.html',myHall=myHall)


@app.route("/chart", methods=["POST", "GET"])
def time_chart():
    if not g.user:
        return redirect(url_for('login'))
    try:
        if request.method == "POST":
            user = request.form["nm"]
            line_labels = Hall.query.filter((Hall.date_stamp == user)).limit(144)
            line_values = Hall.query.filter((Hall.date_stamp == user)).limit(144)
            return render_template('chart2.html', user = user, title='Temperature Graph', max=14, labels=line_labels, values=line_values)
        else:
            return render_template('chart2.html')
    except DataError:
        return render_template('chart2.html', wrong='WRONG DATE')

if __name__ == "__main__":
  app.run(debug=True)
