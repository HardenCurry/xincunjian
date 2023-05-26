from flask import Blueprint


bp=Blueprint("User",__name__,url_prefix="/user")

@bp.route("/login")
def login():
    pass
