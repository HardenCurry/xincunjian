from flask import Blueprint, render_template, request
from models import Food
from exts import db

bp = Blueprint("index", __name__, url_prefix="/index")

#与食品列表与检索有关的
@bp.route("/")
def document():
    # foods = Food.query.all()
    return render_template("index.html", food=foods)
    pass
