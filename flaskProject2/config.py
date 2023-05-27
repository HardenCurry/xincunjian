#session需要加密
SECRET_KEY='asdafsadasdasd'

HOSTNAME="localhost"
PORT=3306
USERNAME="root"
PASSWORD="root"
DATABASE="xingchunjian"

DB_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI=DB_URI #创建db对象，自动读取app.config中的连接信息