#!/usr/bin/env python
#coding=utf-8

import sys
import os
from datetime import timedelta

from flask import Flask, session, request, redirect, send_file, render_template, Response
import flask_login

from privu.model import DBAgent, User
from privu.util import locate_file, get_file_code


default_basedir = os.path.abspath(os.path.dirname(__file__))
default_upload_dir = os.path.join(default_basedir, 'files') # This will be covered by the setting in configuration file.
default_db_dir = os.path.join(default_basedir, 'privu.db')  # This will be covered by the setting in configuration file.
default_username = 'uploader'      # This will be covered by the setting in configuration file.
default_user_password = 'a2FtWkh'  # This will be covered by the setting in configuration file.
default_login_timeout = 5

app = Flask(__name__, template_folder='templates')
app.secret_key = 'dsasdfjahgajdkslfjio34ofk'  # Change this to your secret key
db = DBAgent()
login_manager = flask_login.LoginManager()


def setup_app_config(conf : dict) -> None:
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=conf.get("login_timeout", default_login_timeout))
    app.config["UPLOAD_DIR"] = conf.get("upload_location", default_upload_dir)
    app.config["USER_NAME"] = conf.get("username", default_username)
    app.config["USER_PASSWORD"] = conf.get("userpassword", default_user_password)

    if not os.path.exists(app.config["UPLOAD_DIR"]):
        os.makedirs(app.config["UPLOAD_DIR"])
    db.setup_db(conf.get("database_file_location", conf.get("db_dir", default_db_dir)))
    login_manager.init_app(app)


@login_manager.user_loader
def user_loader(username):
    if username != app.config["USER_NAME"]:
        return

    user = User()
    user.id = username

    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username', '-').strip()
    password = request.form.get('password', '-').strip()

    if username != app.config["USER_NAME"] or password != app.config["USER_PASSWORD"]:
        return

    user = User()
    user.id = username

    return user


@app.route('/', methods=['GET', 'POST'])
def downloadfile():
    if request.method == 'POST':
        filecode = request.form.get('filecode', '').strip()
        if filecode == '':
            return render_template('index.html', message='Please enter file code.')

        filename = db.check_one_code(filecode)
        if filename == '-':
            return render_template('index.html', message='Wrong filecode !!!')

        filepath = locate_file(app, filename)
        return send_file(filepath, as_attachment=True, attachment_filename=filename)
    return render_template('index.html')


@app.route('/uploadfile', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file():
    files = db.find_files()

    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('uploadfile.html', files=files, message="Please choose a file to upload !")

        upfile = request.files['file']
        filename = upfile.filename.strip()

        if filename == '' or filename == '-':
            return render_template('uploadfile.html', files=files, message="Please choose a file to upload !")

        if db.find_one_file(filename) != '-':
            return render_template('uploadfile.html', files=files, message=f"File {filename} already exists !")

        save_filepath = locate_file(app, filename)
        upfile.save(save_filepath)

        try:
            file_code = get_file_code()
            while db.check_one_code(file_code) != '-':
                file_code = get_file_code()
        except:
            raise
            sys.exit(1)

        db.add_one_file(file_code, filename)
        files = db.find_files()
        return render_template('uploadfile.html', files=files, message=f"Save file {filename} successfully !\nGiven file code: {file_code}", msgok=True)
    else:
        return render_template('uploadfile.html', files=files)


@app.route('/deletefile', methods=['POST'])
@flask_login.login_required
def deletefile():
    data = request.get_json(force=True)
    filecode = data.get("filecode", '-')

    filename = db.check_one_code(filecode)
    if filename != '-':
        filepath = locate_file(app, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        db.delete_one_file(filecode)

    return Response('{}',status=200, mimetype='application/json')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form['username']
    userpassword = request.form['password']
    if username == app.config["USER_NAME"] and userpassword == app.config["USER_PASSWORD"]:
        user = User()
        user.id = username
        flask_login.login_user(user)
        session.permanent = True
        return redirect('/uploadfile')

    return render_template('login.html', message="Bad login!")


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return Response('{}',status=200, mimetype='application/json')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect("/login")

