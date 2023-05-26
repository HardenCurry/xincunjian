# 检验是否连接成功，成功则输出“1.”
# with app.app_context():
#     with db.engine.connect() as conn:
#         rs=conn.execute(text("select 1"))
#         print(rs.fetchone())



#
#
# class User1(db.Model):
#     __tablename__="user1"
#
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     username = db.Column(db.String(64), nullable=False)
#     password = db.Column(db.String(256), nullable=False)

# class article(db.Model):
#     __tablename__ = "article"
#     author_id=db.Column(db.integer,db.ForeignKey("user1.id"))
#     author=db.relationship("User1",backref="article")  #=article.author=User.query.get(article.author_id)直接就是这一条记录
#     #backref相当于在User1表中添加了author这一字段即反向一对多







# user=User1(id="1",username="111",password="111")

# with app.app_context():              #简单映射，若改变orm模型用这个同步是不行的
#     db.create_all()
#
#
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

# @app.route('/user/add')                                 #插入
# def add_user():
#     #创建orm对象
#     user = User1(id="1", username="111", password="111")
#     #将orm对象添加到会话中
#     db.session.add(user)
#     #将db.session中的改变同步到数据库中
#     db.session.commit()
#     #返回值
#     return "创建成功"
#
# @app.route('/user/query')                           #查询
# def query_user():
#     #get查找  按主键找
#     # user=User1.query.get(1)
#     # print(f"{user.id}:{user.username}-{user.password}")
#     #filter_by查找   查找多条
#     users=User1.query.filter_by(username="111")
#     for user in users:
#         print(user.username)
#     return "数据查找成功"
#
# @app.route("/user/update")                            #更新
# def update_user():
#     user=User1.query.filter_by(username="111").first()  #无数据返回 ，用  .first（）返回none，  用[0]会报错
#     user.password="2222"
#     #上面步骤相当于存入会话所以不用再存入会话
#     db.session.commit()
#     return "数据修改成功"
#
# @app.route('/user/delete')                      #删除
# def delete_user():
#     #先查
#     user = User1.query.get(1)
#     #后删
#     db.session.delete(user)
#     #在同步
#     db.session.commit()
#     return '删除成功'