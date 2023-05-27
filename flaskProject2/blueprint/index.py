from flask import Blueprint, render_template,request,session
from flask_paginate import get_page_parameter, Pagination
from models import Food
from sqlalchemy import desc
from exts import db


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
    if request.method:
        type=request.form.get('text')
        paixu=request.form.get('paixu')
        if type:
            print('1')
            if type:
                session['type2']=type
                session.permanent = True
            foods1 = Food.query.filter(Food.type2 == type)
            foods1=list(foods1)
            print(foods1)
            # if paixu!=None:
            #     print('px')
            #     if paixu=='升序':
            #         foods1=foods1
            #     else:
            #         print('jxu')
            #         foods1=query.order_by(desc(Food.energy))
            #         print(foods1)
            page = 1
            # 每页显示多少条
            per_page = 10
            # 分页处理
            pagination = Pagination(page=page, per_page=per_page, total=len(foods1), css_framework='bootstrap4')
            # 获取当前页数据
            start = (page - 1) * per_page
            end = start + per_page
            foods1 = foods1[start:end]
            return render_template("index1.html", food=foods1, pagination=pagination, type=type)
        else:
            print('2')
            type = session.get('type2')
            if type:
                type = type
            else:
                type = '主食'
            if paixu!=None:
                print('px')
                if paixu=='升序':
                    session['paixu'] = paixu
                    session.permanent = True
                    foods1=Food.query.filter(Food.type2 == type).order_by(Food.energy)
                else:
                    session['paixu'] = paixu
                    session.permanent = True
                    foods1= Food.query.filter(Food.type2 == type).order_by(desc(Food.energy))
            else:

                paixu=session.get('paixu')
                if paixu == '升序':
                    foods1 = Food.query.filter(Food.type2 == type).order_by(Food.energy)
                elif paixu=='降序':
                    foods1 = Food.query.filter(Food.type2 == type).order_by(Food.energy)
                else:
                    foods1 = Food.query.filter(Food.type2 == type)


            foods1 = list(foods1)
            page = request.args.get(get_page_parameter(), type=int, default=1)
            # 每页显示多少条
            per_page = 10
            # 分页处理
            pagination = Pagination(page=page, per_page=per_page, total=len(foods1), css_framework='bootstrap4')
            # 获取当前页数据
            start = (page - 1) * per_page
            end = start + per_page
            foods1 = foods1[start:end]
            return render_template("index1.html", food=foods1, pagination=pagination, type=type)


