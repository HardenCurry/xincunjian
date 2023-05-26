from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'

    number = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), primary_key=True, unique=True)
    name = db.Column(db.String(255))
    gender = db.Column(db.String(255))
    password = db.Column(db.String(255))
    zhanghao = db.Column(db.String(255))
    phone = db.Column(db.String(255))


class Document(db.Model):
    __tablename__ = 'document'

    dnum = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), primary_key=True, index=True)
    time = db.Column(db.String(255))
    date = db.Column(db.String(255))
    fnum = db.Column(db.String(255))
    weight = db.Column(db.String(255))
    unum = db.Column(db.String(255), index=True)
    energy = db.Column(db.String(255))

# class Fencibiao(db.Model):
#     __tablename__ = 'fencibiao'
#
#     wnum = db.Column(String(255, 'utf8mb4_0900_ai_ci'), primary_key=True, unique=True)
#     word = db.Column(String(255, 'utf8mb4_0900_ai_ci'))
#     fnum = db.Column(String(255, 'utf8mb4_0900_ai_ci'))
#
# class Fencifanwei(db.Model):
#     __tablename__ = 'fencifanwei'
#
#     word=db.Column(String(255, 'utf8mb4_0900_ai_ci'), index=True),
#     began=db.Column(String(255, 'utf8mb4_0900_ai_ci')),
#     down=db.Column(String(255, 'utf8mb4_0900_ai_ci'))
#
#
class Food(db.Model):
    __tablename__ = 'food'

    fnum = db.Column(db.Integer, primary_key=True, unique=True)
    type1 = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), index=True)
    type2 = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'), index=True)
    fname = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    link = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    img = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
    energy = db.Column(db.String(255, 'utf8mb4_0900_ai_ci'))
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
