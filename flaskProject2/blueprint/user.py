from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from exts import db
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
            # 账号是唯一的
            user = User.query.get(zhanghao)
            if not user:
                flash('账号不在数据库')
                return redirect(url_for('user.login'))
            if check_password_hash(user.password, password):
                # 使用cookie
                session['zhanghao'] = user.zhanghao
                return redirect('/')
            else:
                flash('密码错误')
                return redirect(url_for('user.login'))
        else:
            flash('{}'.format(form.errors))
            return redirect(url_for('auth.login'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            gender = form.gender.data
            if gender == '男' or gender == '女':
                zhanghao = form.zhanghao.data
                if not User.query.get(zhanghao):
                    password = form.password.data
                    age = form.age.data
                    bweight = form.bweight.data
                    height = form.height.data
                    phone = form.phone.data
                    user = User(zhanghao=zhanghao, gender=gender, age=age, bweight=bweight, height=height, phone=phone,
                                password=generate_password_hash(password))
                    db.session.add(user)
                    db.session.commit()
                    flash('注册成功')
                    return redirect(url_for("user.login"))
                else:
                    flash('本账号已存在，请重新设置')
                    return redirect(url_for("user.register"))
            else:
                flash('性别只能填男或女')
                return redirect(url_for("user.register"))
        else:
            flash('{}'.format(form.errors))
            return redirect(url_for("user.register"))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('shouye'))
