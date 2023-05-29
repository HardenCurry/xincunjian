from flask import Blueprint, render_template, session, flash, redirect, url_for, request
import datetime
from models import Food, Document
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
    fnums = []
    sum_energy = 0
    all_energy = 0
    fimgs = []
    weights = []
    if not user:
        flash('登录才能使用该功能')
    else:
        doc0 = Document.query.filter(Document.zhanghao == user).all()
        for i in doc0:
            fnums.append(i.fnum)
            weights.append(i.weight)
            food0 = Food.query.filter(Food.fnum == i.fnum).first()
            all_energy += int(food0.energy)

        doc = Document.query.filter(Document.zhanghao == user).filter(Document.time == time).all()
        for i in doc:
            food = Food.query.filter(Food.fnum == i.fnum).first()
            sum_energy += int(food.energy)
            fnames.append(food.fname)
            fimgs.append(food.img)
            fenergies.append(food.energy)
    search=session.get('search')
    searchtype=session.get('searchtype')
    type=session.get('type2')
    paixu=session.get('paixu')
    if search:
        session.pop('search')
    if searchtype:
        session.pop('searchtype')
    if type:
        session.pop('type')
    if paixu:
        session.pop('paixu')
    return render_template("jilu.html", foods=zip(fnames, fimgs, fenergies, fnums, weights), all_energy=all_energy,
                           sum_energy=sum_energy, time=time)


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


# 删除记录
@bp.route("/del_doc", methods=['POST'])
def del_doc():
    fnum = request.form['fnum_btn']
    user = session.get('zhanghao')
    del_fnum = Document.query.filter(Document.zhanghao == user).filter(Document.fnum == fnum).first()
    db.session.delete(del_fnum)
    db.session.commit()
    return redirect(url_for('document.document'))


@bp.route("/update_weight", methods=['POST', 'GET'])
def update_weight():
    fnum = request.form['fnum_btn2']
    weight = request.form[f'{fnum}']
    print(weight, fnum)
    doc=Document.query.filter(Document.fnum==fnum).first()
    doc.weight=weight
    db.session.commit()
    return redirect(url_for('document.document'))
