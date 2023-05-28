from flask import Flask, render_template, session, g
import config
from exts import db
from sqlalchemy import text
from flask_migrate import Migrate
from models import User
from models import Food
from blueprint.user import bp as user_bp
from blueprint.document import bp as document_bp
from blueprint.index import bp as index_bp
from blueprint.search import bp as search_bp
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(document_bp)
app.register_blueprint(index_bp)
app.register_blueprint(search_bp)

migrate = Migrate(app, db)


# 1.flask db init 只执行一次在终端
# 2.flask db migrate  识别orm改变生成迁移脚本
# 3.flask db upgrade 同步迁移脚本到数据库中

@app.route("/")
def shouye():
    return render_template('shouye.html')
@app.route('/jilu')
def test():
    return render_template('jilu.html')


@app.before_request
def my_before_request():
    user_zhanghao = session.get('zhanghao')
    if user_zhanghao:
        user = User.query.filter_by(zhanghao=user_zhanghao).first()
        setattr(g, 'user', user)
    else:
        setattr(g, 'user', None)

#所有模板中能用该变量
@app.context_processor
def my_context_processor():
    return {'user':g.user}


if __name__ == '__main__':
    app.run()
