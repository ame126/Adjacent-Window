from flask import Flask, render_template, session, request, redirect, url_for, jsonify, make_response
import flask
import flask_login
from datetime import timedelta
from werkzeug.utils import secure_filename

import os

'''Initialise the flask app '''
app = Flask(__name__)


app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

UPLOAD_FOLDER = '\\storage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
logged_in = False

login_cred = {
    "testuser1": "test123",
    "testuser2": "test456",
    "testuser3": "test789"
}


def clear_session():
    """
    Clears the session variables
    Args: None
    :return:  None
    """
    session.pop('username', default=None)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    global logged_in
    logged_in = True
    if request.method == 'POST':
        username = request.form.get('username')  # access the data inside
        password = request.form.get('password')
        session['username'] = username

        if username not in login_cred:
            return render_template('login.html', message="Invalid username/password")

        elif login_cred[username] != password:
            return render_template('login.html', message="Invalid username/password")
        else:
            flask.flash("Logged in Successfully")
            return render_template("index.html")
    else:
        return render_template('login.html')


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


@app.route('/logout/<username>', methods=['GET', 'POST'])
def logout(username):
    session.pop(username)
    print(session.keys())


@app.errorhandler(404)
def handle_bad_request(e):
    """
    Handle error codes and relevant pages
    """
    return render_template("error.html")


@app.route('/signup', methods = ['POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username in session:
            return render_template('login.html', message="Username already signedin")
        else:
            #new user
            session['username'] = username
            login_cred[username] = password
            return render_template("index.html", message = "Successfully registered")


@app.route('/', methods=['GET', 'POST'])
# @flask_login.login_required
def main():
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(host="localhost", port=5000)
