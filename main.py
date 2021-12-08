import mysql.connector
import os
import json
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from mysql.connector.errors import Error
from datetime import timedelta
from config import Config

'''Initialise the flask app '''
app = Flask(__name__)

app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

UPLOAD_FOLDER = '\\storage'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
logged_in = False

config_object = Config()
login_cred = {
    "testuser1": "test123",
    "testuser2": "test456",
    "testuser3": "test789"
}


def create_db():
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user=config_object.dbuser,
            password=config_object.dbpassword,
            port=config_object.dbport,
            auth_plugin=config_object.authplugin,
            database=config_object.database
        )

        cursor = mydb.cursor()
        query = "Select * from " + config_object.database + ";"
        cursor.execute(query)
        results = cursor.fetchall()

    except Error as err:
        print("Error code: ", err.errno)
        print("Message", err.msg)


def convert_to_string(data):
    # print(data.keys())
    for keys in data:
        temp_val = "*#*".join(data[keys])
        data[keys] = "'" + temp_val + "'"
    return data


def record_exists(username):
    try:
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user=config_object.dbuser,
            password=config_object.dbpassword,
            port=int(config_object.dbport),
            auth_plugin=config_object.authplugin,
            database=config_object.database
        )

        cursor = mydb.cursor()
        query = "select count(*) from userfiles where username = '" + username + "';"
        cursor.execute(query)
        results = cursor.fetchall()
        mydb.close()
        return results[0][0] > 0
    except:
        print("Error for record check")


@app.route("/save_files", methods=['POST'])
def insert_record():
    data = request.get_json()

    data_transformed = convert_to_string(data)
    username = session['username']
    if not record_exists(username):
        # insert
        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user=config_object.dbuser,
                password=config_object.dbpassword,
                port=int(config_object.dbport),
                auth_plugin=config_object.authplugin,
                database=config_object.database
            )

            cursor = mydb.cursor()
            query = "INSERT INTO userfiles" + " (username, images, videos, documents, presentation)" + " VALUES (" + \
                    "'" + session['username'] + "'," + data_transformed['images'] + "," + data_transformed[
                        'videos'] + "," + \
                    data_transformed['docs'] + "," + data_transformed['presentation'] + ");"
            cursor.execute(query)
            mydb.commit()
            # results = cursor.fetchall()
            mydb.close()
            return jsonify(sucess=True)
        except Error as err:
            print("Error code: ", err.errno)
            print("Message", err.msg)
    else:
        # update record
        # print("Updated record for username")
        print(data_transformed['presentation'])
        try:
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user=config_object.dbuser,
                password=config_object.dbpassword,
                port=int(config_object.dbport),
                auth_plugin=config_object.authplugin,
                database=config_object.database
            )

            cursor = mydb.cursor()
            query = "UPDATE userfiles " + "SET images = " + data_transformed['images'] + ", videos = " + \
                    data_transformed[
                        'videos'] + ", documents = " + data_transformed['docs'] + ", presentation = " + data_transformed['presentation'] + " WHERE username = '" + username + "';"

            cursor.execute(query)
            mydb.commit()
            # results = cursor.fetchall()
            mydb.close()

        except:
            print("Error updating")
        return jsonify(success=True)


def clear_session():
    """
    Clears the session variables
    Args: None
    :return:  None
    """
    session.pop('username', default=None)


def get_mysql_connector():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        user=config_object.dbuser,
        password=config_object.dbpassword,
        port=int(config_object.dbport),
        auth_plugin=config_object.authplugin,
        database=config_object.database
    )

    return mydb


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')  # access the data inside
        password = request.form.get('password')
        session['username'] = username

        if username not in login_cred:
            return render_template('login.html', message="Invalid username/password")

        elif login_cred[username] != password:
            return render_template('login.html', message="Invalid username/password")
        else:
            return render_template('default.html')
    else:
        return render_template('login.html')


@app.route("/retrieve", methods=['GET'])
def retrieve_data():
    username = session['username']
    mydb = get_mysql_connector()
    query = "SELECT images, videos, documents, presentation from userfiles WHERE username = '" + session['username'] + "';"
    cursor = mydb.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    data = {'images': results[0][0], 'videos': results[0][1], 'documents': results[0][2],
            'presentation': results[0][3]}
    return render_template("index.html", data=json.dumps(data))



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/logout/<username>', methods=['GET', 'POST'])
def logout(username):
    session.pop(username)



@app.errorhandler(Exception)
def handle_bad_request(e):
    """
    Handle error codes and relevant pages
    """
    return render_template("error.html")


@app.route('/signup', methods=['POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username in session:
            return render_template('login.html', message="Username already signedin")
        else:
            # new user
            session['username'] = username
            login_cred[username] = password
            return render_template("index.html", message="Successfully registered")


@app.route('/', methods=['GET', 'POST'])
# @flask_login.login_required
def main():
    if "username" not in session:
        return redirect(url_for("login"))
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(host="localhost", port=5000)
