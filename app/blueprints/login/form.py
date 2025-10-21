import wtforms
from wtforms.validators import Length
from app.models import User
#登入表单
class LoginForms(wtforms.Form):
    email=wtforms.StringField(label="邮箱", validators=[wtforms.validators.Email(message="邮箱格式不正确")])
    password=wtforms.StringField(label="密码", validators=[Length(min=6, max=50, message="密码格式错误")])

    def validate_email(self,field):
        email=field.data
        user=User.query.filter_by(email=email).first()
        if not user:
            raise wtforms.ValidationError("邮箱不存在，请先注册")
    
    def validate_password(self, field):
        password=field.data
        email=self.email.data
        user=User.query.filter_by(email=email,password=password).first()
        if user.password != password:
            raise wtforms.ValidationError("邮箱或密码不正确")