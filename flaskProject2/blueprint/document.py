from flask import Blueprint, render_template, session, flash, redirect, url_for, request
import datetime
from models import Food, Document, User
from exts import db

bp = Blueprint("document", __name__, url_prefix="/document")


# 修改年龄，体重，身高
@bp.route('/update_userinfo', methods=['POST'])
def update_userinfo():
    user = session.get('zhanghao')
    age = request.form['age']
    bweight = request.form['bweight']
    height = request.form['height']
    coef = request.form['coef']
    session['coef'] = coef

    user_data = User.query.filter(User.zhanghao == user).first()
    user_data.age = age
    user_data.bweight = bweight
    user_data.height = height
    db.session.commit()
    return redirect(url_for('document.document'))


# 显示user的记录
@bp.route("/", methods=['POST', 'GET'])
def document():
    user = session.get('zhanghao')
    time = request.args.get('time')
    if not time:
        # 不是按button
        if not session.get('time'):
            # 第一次进入
            time = '早'
            session['time'] = time
        else:
            time = session.get('time')
    else:
        session['time'] = time

    fnames = []
    fenergies = []
    fnums = []
    sum_energy = 0
    all_energy = 0
    fimgs = []
    weights = []
    if not user:
        flash('登录才能使用该功能')
        return render_template('shouye.html')
    else:
        # all_energy 计算总卡路里
        doc0 = Document.query.filter(Document.zhanghao == user).all()
        for i in doc0:
            food = Food.query.filter(Food.fnum == i.fnum).first()
            all_energy += (round(int(food.energy) * i.weight * 0.01))

        # 符合time的记录
        doc = Document.query.filter(Document.zhanghao == user).filter(Document.time == time).all()
        for i in doc:
            fnums.append(i.fnum)
            weights.append(i.weight)
            food = Food.query.filter(Food.fnum == i.fnum).first()
            sum_energy += round(int(food.energy) * i.weight * 0.01)
            fnames.append(food.fname)
            fimgs.append(food.img)
            fenergies.append(round(int(food.energy) * i.weight * 0.01))
        # 用户信息
        user_data = User.query.filter(User.zhanghao == user).first()
        age = user_data.age
        bweight = user_data.bweight
        height = user_data.height
        info = {}
        info['age'] = age
        info['bweight'] = bweight
        info['height'] = height
        # BMR计算
        # 男性BMR=66+13.7*体重（Kg）+5*身高（cm）-6.8*年龄（周岁）
        # 女性BMR=655+9.6*体重（Kg）+1.7*身高（cm）-4.7*年龄（周岁）
        gender = user_data.gender
        if not session.get('coef'):
            coef = 1.0
        else:
            coef = session['coef']
        if gender == '男':
            bmr = 66 + 13.7 * bweight + 5 * height - 6.8 * age
        else:
            bmr = 655 + 9.6 * bweight + 1.7 * height - 4.7 * age
        target = float(coef) * bmr
        selected=['' for i in range(6)]
        res=round((float(coef)-1)/0.2)
        selected[res]='selected='
        print(selected)


        search = session.get('search')
        searchtype = session.get('searchtype')
        type = session.get('type')
        paixu = session.get('paixu')
        if search:
            session.pop('search')
        if searchtype:
            session.pop('searchtype')
        if type:
            session.pop('type2')
        if paixu:
            session.pop('paixu')
        return render_template("jilu.html", foods=zip(fnames, fimgs, fenergies, fnums, weights), all_energy=all_energy,
                               sum_energy=sum_energy, time=time, info=info, target=target,selected=selected)

    # 选好食品并存到Document中
    @bp.route("/<fnum>", methods=['POST', 'GET'])
    def document1(fnum):
        user = session.get('zhanghao')
        time = session.get('time')
        if not time:
            time = '早'
        session['time'] = time
        if not user:
            flash('登录才能使用该功能')
            return render_template('shouye.html')
        else:
            date = datetime.datetime.now()
            x = '{:%Y-%m-%d}'.format(date)
            doc0 = Document.query.filter(Document.zhanghao == user).filter(Document.time == time).all()
            for i in doc0:
                if i.fnum == fnum:
                    flash('此食品已在记录中，不能重复添加')
                    return redirect(url_for('document.document'))
            doc = Document(zhanghao=user, fnum=fnum, weight=100, date=x, time=time)
            db.session.add(doc)
            db.session.commit()
            return redirect(url_for('document.document'))

    # 删除记录
    @bp.route("/del_doc", methods=['POST'])
    def del_doc():
        fnum = request.form['fnum_btn']
        user = session.get('zhanghao')
        time = session.get('time')
        del_fnum = Document.query.filter(Document.zhanghao == user).filter(Document.fnum == fnum).filter(
            Document.time == time).first()
        db.session.delete(del_fnum)
        db.session.commit()
        return redirect(url_for('document.document'))

    @bp.route("/update_weight", methods=['POST', 'GET'])
    def update_weight():
        fnum = request.form['fnum_btn2']
        weight = request.form[f'{fnum}']
        time = session.get('time')
        doc = Document.query.filter(Document.fnum == fnum).filter(Document.time == time).first()
        doc.weight = weight
        db.session.commit()
        return redirect(url_for('document.document'))
