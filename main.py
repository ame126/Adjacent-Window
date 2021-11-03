from flask import Flask, render_template, session, request, redirect, url_for, jsonify, make_response
from flask_bootstrap import Bootstrap
import flask
import flask_login
from datetime import timedelta
from werkzeug.utils import secure_filename

import os

'''Initialise the flask app '''
app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

UPLOAD_FOLDER = '\\storage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
logged_in = False


@app.route('/login/', methods=['GET', 'POST'])
def login():
    global logged_in
    logged_in = True
    if request.method == 'POST':
        username = request.form.get('username')  # access the data inside
        password = request.form.get('password')

        if username == 'testuser' and password == 'test123':
            flask.flash("Logged in Successfully")
            return render_template("index.html")
        else:
            flask.flash("Invalid username/password")
    return render_template('login.html', message ="Invalid username/password")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flask.flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flask.flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, filename))
            # flask.flash(f'{filename.rsplit(".",1)[1]}File Uploaded Successfully')
        return jsonify(success=True)
    return jsonify(success=True)



@app.route('/logout/<username>', methods=['GET','POST'])
def logout(username):
    session.pop(username)
    print(session.keys())


"""
Handle error codes and relevant pages
"""
@app.errorhandler(404)
def handle_bad_request(e):
    return render_template("error.html")


@app.route('/', methods=['GET', 'POST'])
# @flask_login.login_required
def main():
    global logged_in
    if not logged_in:
        return redirect(url_for("login"))
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(host="localhost", port=5000)
