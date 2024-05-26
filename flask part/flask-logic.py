# from datetime import date, time
# from doctest import master
# import flask
# from flask import Flask, request, redirect, url_for
# import sqlite3
# from sqlite3 import connect, Connection
# import flask_login
# from flask_login import LoginManager, UserMixin, login_user
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField
# from wtforms.validators import DataRequired
# from werkzeug.utils import url_has_allowed_host_and_scheme

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Login')

# con = connect('my_database.db')
# cur = Connection.cursor()
# con1 = connect('my_database_order.db')
# cur1 = Connection.cursor()
# con2 = connect('my_database_masters.db')
# cur2 = Connection.cursor()
# app = Flask(__name__)

# @app.route('/register.html', methods=['POST'])
# def reg():
#     username = request.form['username']
#     password = request.form['password']
#     user = User(username=username, password = password)
#     cur.execute(''' CREATE TABLE IF NOT EXISTS Users(id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL) ''')
#     con.commit()
#     con.close()
#     return redirect(url_for('register'))



# login_manager = LoginManager()
# login_manager.init_app(app)
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

# class User(UserMixin):
#      def __init__(self, id):
#           self.id = id
# @login_manager.user_loader
# def user_loader(id):
#      return User.get(id, None)

# @app.route('/login.html', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Создаем экземпляр класса User
#         user = User(form.user_id.data)
#         login_user(user)
#         flask.flash('logged in successfully')
#         next = flask.request.args.get('next')
#         if not url_has_allowed_host_and_scheme(next, request.host):
#             return flask.abort(400)
#         return flask.redirect(next or flask.url_for('index.html'))
#     return flask.render_template('login.html', form=form)


# @app.route('/', methods=['GET', 'POST'])
# def order():
#     cur1.execute(''' CREATE TABLE IF NOT EXISTS Datatime(date INTEGER, time INTEGER) ''')
#     cur1.commit()
#     cur1.close()
#     if request.method == 'POST':
#         date = request.form['date']
#         time = request.form['time']
#         cur1.execute(''' INSERT INTO my_database_order (date, time) VALUES (?, ?) ''', (date, time))
#         cur1.commit()
#         cur1.close()
#     def check_datatime(db_path):
#          global time
#          cur1.execute(''' SELECT * FROM my_database_order WHERE time =? ''', (time))
#          result = con1.fetchone()
#          cur1.commit()
#          cur1.close()
#          if result:
#               return True
#          else:
#               return False
#          if check_datatime(db_path, time):
#             return flask.render_template('order.html', form=form)
# @app.route('/', methods=['GET'])
# def insert():
#      cur1.execute(''' SELECT * FROM my_database_order WHERE date =?, time=? ''', (date, time))
#      cur1.commit()
#      cur1.close()
#      cur2.execute(''' CREATE TABLE IF NOT EXCISTS, Masters(master TEXT TO NULL) ''')
#      cur2.execute(''' SELECT * FROM my_database_masters WHERE master=? ''', master)
#      cur2.commit()
#      cur2.close()
#      return flask.render_template(flask.urlfor('profile'))
# if __name__ == '__main__':
#         app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SECRET_KEY'] = 'secret_key23123'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'], method='sha256')
        new_user = User(username=request.form['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация прошла успешно!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            if check_password_hash(user.password, request.form['password']):
                resp = make_response(redirect(url_for('profile')))
                if 'remember' in request.form:
                    expires = datetime.datetime.now()
                    expires = expires + datetime.timedelta(days=30)
                    resp.set_cookie('username', request.form['username'], expires=expires)
                    resp.set_cookie('password', request.form['password'], expires=expires)
                return resp
        flash('Пожалуйста, проверьте свои данные и попробуйте еще раз.')
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
