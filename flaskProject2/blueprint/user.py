from flask import Blueprint, render_template, redirect, url_for, session
from exts import db
from flask_mail import Message
from flask import request
import string
import random
from .forms import RegisterForm, LoginForm
from models import User
# 对密码加密
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            zhanghao = form.zhanghao.data
            password = form.password.data
            #账号是唯一的
            user = User.query.filter_by(zhanghao=zhanghao).first()
            if not user:
                print('账号不在数据库')
                return redirect(url_for('user.login'))
            if check_password_hash(user.password, password):
                #使用cookie
                session['user_zhanghao'] = user.zhanghao
                return redirect('/')
            else:
                print('密码错误')
                return redirect(url_for('user.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            zhanghao = form.zhanghao.data
            password = form.password.data
            gender = form.gender.data
            phone = form.phone.data
            user = User(zhanghao=zhanghao, gender=gender, phone=phone, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user.login"))
        else:
            print(form.errors)
            return redirect(url_for("user.register"))
