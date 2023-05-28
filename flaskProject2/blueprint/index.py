from flask import Blueprint, render_template,request,session
from flask_paginate import get_page_parameter, Pagination
from models import Food
from sqlalchemy import desc
from exts import db


def fenye(foods,a):
    foods = list(foods)
    if a==0:
        page = request.args.get(get_page_parameter(), type=int, default=1)
    else:
        page=1
    # 每页显示多少条
    per_page = 10
    # 分页处理
    pagination = Pagination(page=page, per_page=per_page, total=len(foods), css_framework='bootstrap4')
    # 获取当前页数据
    start = (page - 1) * per_page
    end = start + per_page
    return foods[start:end],pagination


bp=Blueprint("index",__name__,url_prefix="/")

@bp.route("/")
def document2():
    return render_template("shouye.html")
    pass


@bp.route("/index")
def document():
    foods=Food.query.filter(Food.type2=='主食')
    session['type2'] = '主食'
    session.permanent = True
    foods=list(foods)
    #获取当前页码
    page = request.args.get(get_page_parameter(), type=int, default=1)
    #每页显示多少条
    per_page=10
    #分页处理
    pagination = Pagination(page=page, per_page=per_page, total=len(foods), css_framework='bootstrap4')
    #获取当前页数据
    start = (page - 1) * per_page
    end = start + per_page
    foods= foods[start:end]
    return render_template("index.html",food=foods,pagination=pagination)

@bp.route("/index1", methods=['POST', 'GET'])
def document1():
    type=request.form.get('text')
    paixu=request.form.get('paixu')
    g = 0
    if type:
        session['type2'] = type
        g = 1
    if paixu:
        session['paixu'] = paixu
        g = 1
    #如果现在点击分类
    if type:
        print('1')
        if type:
            session['type2']=type
            session.permanent = True
        foods = Food.query.filter(Food.type2 == type)

        # if paixu!=None:
        #     print('px')
        #     if paixu=='升序':
        #         foods1=foods1
        #     else:
        #         print('jxu')
        #         foods1=query.order_by(desc(Food.energy))
        #         print(foods1)
        foods,pagination=fenye(foods,g)
        return render_template("index1.html", food=foods, pagination=pagination, type=type)
    #如果没有点击分类
    else:

        print('2')
        type = session.get('type2')
        if type:
            type = type
            g = 0
        else:
            type = '主食'
            g=1
        #如果现在有点击排序
        if paixu!=None:
            g=1
            print('px')
            if paixu=='升序':
                session['paixu'] = paixu
                session.permanent = True
                foods=Food.query.filter(Food.type2 == type).order_by(Food.energy)
            else:
                session['paixu'] = paixu
                session.permanent = True
                foods= Food.query.filter(Food.type2 == type).order_by(desc(Food.energy))
        #如果没有点击排序但之前有
        else:
            paixu=session.get('paixu')

            if paixu == '升序':
                foods = Food.query.filter(Food.type2 == type).order_by(Food.energy)
                g=0
            elif paixu=='降序':
                foods = Food.query.filter(Food.type2 == type).order_by(desc(Food.energy))
                g=0
            else:
                foods = Food.query.filter(Food.type2 == type)
                g=0


        foods,pagination=fenye(foods,g)
        return render_template("index1.html", food=foods, pagination=pagination, type=type)


