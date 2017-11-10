from flask import Flask
from flask import render_template
from flask import request
import os

app = Flask(__name__)
data_base = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/about')
def about():
    return data_base

@app.route('/login')
def login():
     return render_template('login.html',name=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return  render_template('register.html')
    else:
        return 'post'


if __name__ == '__main__':
    app.run(debug=True)
