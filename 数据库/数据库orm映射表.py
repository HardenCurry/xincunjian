
#column前需要加db.       db.column


class User(db.Model):
    __tablename__ = 'user'

    number = Column(String(255, 'utf8mb4_0900_ai_ci'), primary_key=True, unique=True)
    name = Column(String(255))
    gender = Column(String(255))
    password = Column(String(255))
    zhanghao = Column(String(255))
    phone = Column(String(255))


class Document(db.Model):
    __tablename__ = 'document'

    dnum = Column(String(255, 'utf8mb4_0900_ai_ci'), primary_key=True, index=True)
    time = Column(String(255))
    date = Column(String(255))
    fnum = Column(String(255))
    weight = Column(String(255))
    unum = Column(String(255), index=True)
    energy = Column(String(255))

class Fencibiao(db.Model):
    __tablename__ = 'fencibiao'

    wnum = Column(String(255, 'utf8mb4_0900_ai_ci'), primary_key=True, unique=True)
    word = Column(String(255, 'utf8mb4_0900_ai_ci'))
    fnum = Column(String(255, 'utf8mb4_0900_ai_ci'))

class Fencifanwei(db.Model):
    __tablename__ = 'fencifanwei'

    Column('word', String(255, 'utf8mb4_0900_ai_ci'), index=True),
    Column('began', String(255, 'utf8mb4_0900_ai_ci')),
    Column('down', String(255, 'utf8mb4_0900_ai_ci'))


class Food(db.Model):
    __tablename__ = 'food'

    fnum = Column(Integer, primary_key=True, unique=True)
    type1 = Column(String(255, 'utf8mb4_0900_ai_ci'), index=True)
    type2 = Column(String(255, 'utf8mb4_0900_ai_ci'), index=True)
    fname = Column(String(255, 'utf8mb4_0900_ai_ci'))
    link = Column(String(255, 'utf8mb4_0900_ai_ci'))
    img = Column(String(255, 'utf8mb4_0900_ai_ci'))
    energy = Column(String(255, 'utf8mb4_0900_ai_ci'))

class Jiansuo(db.Model):
    __tablename__ = 'jiansuo'

    jnum = Column(Integer, primary_key=True, unique=True)
    unum = Column(Integer)
    date = Column(String(255))



