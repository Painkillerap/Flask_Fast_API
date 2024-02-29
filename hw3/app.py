from flask import Flask, redirect, render_template, request, session, url_for

import hashlib
import os

from flask import Flask, redirect, render_template, request, session, url_for

from forms import RegistrationForm, LoginForm
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_base.db'
app.config['SECRET_KEY'] = b'7a11a569dc37d6df1a6f75d743fc4590cc2ad62e59096ab1e2a9efc0c1ca36d4'
db.init_app(app)


@app.cli.command('init-db')
def init_db():
    db.create_all()


def hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 1_000_000)
    return key, salt


def check_user(email):
    if User.query.filter((User.email == email)).first():
        return True
    return False


def check_login(email, password):
    if check_user(email):
        extention_user = User.query.filter((User.email == email)).first()
        user_salt = extention_user.salt
        user_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), user_salt, 1_000_000)
        if user_password == extention_user.password:
            return True
    return False


@app.route('/')
@app.route('/index/')
def index():
    if 'email' in session:
        autorization = session['name']
    else:
        autorization = None
    return render_template("index.html", autorization=autorization, title='Домашнее задание 3')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password, salt = hash_password(form.password.data)
        if check_user(email):
            error_msg = 'Пользователь с таким e-mail уже существует!'
            form.name.errors.append(error_msg)
            return render_template("registration.html", form=form, title='Регистрация')
        user = User(name=name, surname=surname, email=email, password=password, salt=salt)
        db.session.add(user)
        db.session.commit()
        return render_template("registration_sucsess.html", title='Регистрация завершена')
    return render_template("registration.html", form=form, title='Регистрация')


@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        if check_login(email, password):
            extention_user = User.query.filter((User.email == email)).first()
            session['email'] = extention_user.email
            session['name'] = extention_user.name
            return redirect(url_for('cabinet'))
        error_msg = 'Неверный e-mail или пароль!'
        form.email.errors.append(error_msg)
    return render_template("login.html", form=form, title='Вход в личный кабинет')


@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/cabinet/')
def cabinet():
    if 'email' in session:
        return render_template("cabinet.html", title='Личный кабинет', name=session['name'], email=session['email'])
    else:
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
