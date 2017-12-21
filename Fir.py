from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from flask_login import login_user
from flask_login import LoginManager
from flask_login import login_required
from flask_login import current_user

from flask_uploads import  *
from User import User
from DataBase import DataBase
import os

from biplist import *
import base64


def defualtDest(app):
    return UploadDir

current_dir = os.path.dirname(os.path.abspath(__file__))
UploadDir = os.path.join(os.path.join(current_dir,'static'),'upload')
attachement = UploadSet('ipa',('ipa','apk'),default_dest=defualtDest)

app = Flask(__name__)
app.secret_key = '2323432'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/home')
def home():
    return str(DataBase.getAllApplication())


@app.route('/about')
@login_required
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', hiddenLoginButton=True)
    else:
        form = request.form
        user = User.getUser(form['username'], form['password'])
        if user != None:
            login_user(user)
            return jsonify({'code': 200})
        else:
            return jsonify({'code': 100, 'msg': '账号密码错误'})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', hiddenLoginButton=True)
    else:
        form = request.form
        username = form['username']
        password = form['password']
        isExist = User.findUser(username)
        if isExist:
            return jsonify({'code': 100, 'msg': '账号已被注册'})
        else:
            User.register(username=username, password=password)
            return jsonify({'code': 200, 'msg': '注册成功'})


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template('upload.html', user=current_user)
    else:
        file = request.files['file_data']
        filename = attachement.save(file)
        form = request.form
        DataBase.saveApp(form['id'],form['name'],form['version'],form['info'],filename,current_user.user_id)
        return  jsonify({'code': 200, 'msg': '上传成功'})


@app.route('/parse', methods=['POST'])
@login_required
def parse():
    form = request.form
    content = form['content']
    i = readPlistFromString(base64.b64decode(content))

    return jsonify({'code': 200,
                    'name': i['CFBundleDisplayName'],
                    'shortversion': i['CFBundleShortVersionString'],
                    'version':i['CFBundleVersion'],
                    'id':i['CFBundleIdentifier']})


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    configure_uploads(app, (attachement))
    app.run(debug=True)


    # app.run(debug=True,ssl_context=('/Users/virgil/Desktop/test1/server.crt', '/Users/virgil/Desktop/test1/server.key'))
