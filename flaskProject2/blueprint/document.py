from flask import Blueprint, render_template,request,session
from flask_paginate import get_page_parameter, Pagination
from models import Food
from sqlalchemy import desc
from exts import db

bp=Blueprint("document",__name__,url_prefix="/document")

@bp.route("/", methods=['POST', 'GET'])
def document():

    return render_template("sol2.html")
#获取选定食物存入会话中
@bp.route("/<fnum>", methods=['POST', 'GET'])
def document1(fnum):
    print(fnum)
    foods = Food.query.filter(Food.fnum == fnum).all()
    for i in foods:
        fname=i.fname
        energy=i.energy
    session['fname']=fname
    session['energy']=energy
    print(fname,energy)
    return render_template("sol2.html")

