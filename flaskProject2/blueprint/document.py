from flask import Blueprint, render_template, session, flash, redirect, url_for, request
import datetime
from flask_paginate import get_page_parameter, Pagination
from models import Food, Document
from sqlalchemy import desc
from exts import db

bp = Blueprint("document", __name__, url_prefix="/document")


# 显示user的记录
@bp.route("/", methods=['POST', 'GET'])
def document():
    user = session.get('zhanghao')
    time = request.args.get('time')
    session['time'] = time
    if not time:
        time = '早'
    fnames = []
    fenergies = []
    sum_energy = 0
    all_energy=0
    fimgs = []
    if not user:
        flash('登录才能使用该功能')
    else:
        doc0 = Document.query.filter(Document.zhanghao == user).all()
        for i in doc0:
            food0 = Food.query.filter(Food.fnum == i.fnum).first()
            all_energy += int(food0.energy)

        doc = Document.query.filter(Document.zhanghao == user).filter(Document.time == time).all()
        for i in doc:
            food = Food.query.filter(Food.fnum == i.fnum).first()
            sum_energy += int(food.energy)
            fnames.append(food.fname)
            fimgs.append(food.img)
            fenergies.append(food.energy)
    return render_template("jilu.html", foods=zip(fnames, fimgs, fenergies), all_energy=all_energy,sum_energy=sum_energy,time=time)


# 选好食品并存到Document中
@bp.route("/<fnum>", methods=['POST', 'GET'])
def document1(fnum):
    user = session.get('zhanghao')
    time = session.get('time')
    if not time:
        time = '早'
    if not user:
        flash('登录才能使用该功能')
    else:
        date = datetime.datetime.now()
        x = '{:%Y-%m-%d}'.format(date)
        print(x)
        doc = Document(zhanghao=user, fnum=fnum, weight=100, date=x, time=time)
        db.session.add(doc)
        db.session.commit()
        return redirect(url_for('document.document'))
