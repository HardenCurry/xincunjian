from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'

    zhanghao = db.Column(db.String(255), primary_key=True, nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    bweight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)



class Document(db.Model):
    __tablename__ = 'document'

    dnum = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(255))
    date = db.Column(db.DateTime)   
    fnum = db.Column(db.String(255))
    weight = db.Column(db.Integer)
    zhanghao = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), index=True)


class Fencibiao(db.Model):
    __tablename__ = 'fencibiao'

    wnum = db.Column(db.Integer, primary_key=True, unique=True)
    word = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    fnum = db.Column(db.Integer)


class Fencifanwei(db.Model):
    __tablename__ = 'fencifanwei'

    wid = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), index=True)
    began = db.Column(db.Integer)
    down = db.Column(db.Integer)


class Food(db.Model):
    __tablename__ = 'food'

    fnum = db.Column(db.Integer, primary_key=True, unique=True)
    type1 = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), index=True)
    type2 = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), index=True)
    fname = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    link = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    img = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    energy = db.Column(db.Integer)
    ts = db.Column(db.Integer)
    zf = db.Column(db.Integer)
    dbz = db.Column(db.Integer)
    qws = db.Column(db.Integer)
#
# class Jiansuo(db.Model):
#     __tablename__ = 'jiansuo'
#
#     jnum = db.Column(Integer, primary_key=True, unique=True)
#     unum =db.Column(Integer)
#     date = db.Column(String(255))
#
#
#
