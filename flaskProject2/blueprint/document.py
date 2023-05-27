from flask import Blueprint,render_template

bp=Blueprint("document",__name__,url_prefix="/document")

#与记录有关的网页
@bp.route("/")
def document():
    return render_template("sol2.html")


@bp.route("/1.html")
def zao():
    return render_template("1.html")
