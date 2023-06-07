import wtforms
from wtforms.validators import Length,EqualTo

class RegisterForm(wtforms.Form):
    zhanghao = wtforms.StringField(validators=[Length(min=3, max=12, message="账号格式错误！")])
    gender = wtforms.StringField(validators=[Length(min=1, max=1, message="性别格式错误！")])
    age = wtforms.IntegerField()
    bweight = wtforms.IntegerField()
    height = wtforms.IntegerField()
    phone = wtforms.StringField(validators=[Length(min=4, max=12, message="电话号码格式错误！")])
    password = wtforms.StringField(validators=[Length(min=4, max=12, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

class LoginForm(wtforms.Form):
    zhanghao = wtforms.StringField(validators=[Length(min=1, max=12, message="账号格式错误！")])
    password = wtforms.StringField(validators=[Length(min=1, max=12, message="密码格式错误！")])