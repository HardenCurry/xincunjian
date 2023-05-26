from flask import Blueprint, render_template,request
from models import Food
from exts import db

bp=Blueprint("index",__name__,url_prefix="/")

@bp.route("/")
def document():
    foods=Food.query.all()
    return render_template("index.html",food=foods)
    pass

