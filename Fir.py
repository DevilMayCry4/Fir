from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from flask_login import login_user
from flask_login import LoginManager
from flask_login import login_required
from flask import g
from User import User
from DataBase import DataBase

app = Flask(__name__)
app.secret_key = '2323432'
login_manager = LoginManager()
login_manager.login_view='login'
login_manager.init_app(app)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
@app.route('/home')
def  home():
    return str(DataBase.getAllApplication())

@app.route('/about')
@login_required
def about():
    return  render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
     return render_template('login.html',hiddenLoginButton=True)
    else:
        form = request.form
        user = User.getUser(form['username'],form['password'])
        if user != None:
            login_user(user)
            return  jsonify({'code':200})
        else:
            return  jsonify({'code':100,'msg':'账号密码错误'})

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return  render_template('register.html',hiddenLoginButton=True)
    else:
        form = request.form
        username = form['username']
        password = form['password']
        isExist = User.findUser(username)
        if isExist:
            return jsonify({'code': 100,'msg':'账号已被注册'})
        else:
            User.register(username=username,password=password)
            return jsonify({'code': 200, 'msg': '注册成功'})


@app.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        return  ''


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(debug=True,ssl_context=('/Users/virgil/Desktop/test1/server.crt', '/Users/virgil/Desktop/test1/server.key'))

