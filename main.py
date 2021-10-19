from flask import Flask, render_template
# from flask.ext.scss import Scss

'''Initialise the flask app '''
app = Flask(__name__)
# Scss(app)
@app.route('/')
def main():
    return render_template("index.html")



if __name__ == '__main__':
    app.run()