import wtforms
from wtforms.validators import Length
from app.models import EmailCaptcha, User

#注册表单
class RegisterForms(wtforms.Form):
    email=wtforms.StringField(label="邮箱",validators=[wtforms.validators.Email(message="邮箱格式不正确")])
    captcha=wtforms.StringField(label="验证码", validators=[Length(min=4,max=4,message="验证码格式错误")])
    username=wtforms.StringField(label="用户名", validators=[Length(min=3, max=20, message="用户名格式错误")])
    password=wtforms.StringField(label="密码", validators=[Length(min=6, max=50, message="密码格式错误")])

    def validate_email(self, field):
        email=field.data
        user=User.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError("邮箱已经注册")
        
    def validate_captcha(self, field):
        captcha=field.data
        email=self.email.data
        captcha_db=EmailCaptcha.query.filter_by(email=email,captcha=captcha).first()
        if not captcha_db:
            raise wtforms.ValidationError("验证码错误")
