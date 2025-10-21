import email
import wtforms
from wtforms.validators import Length,Regexp
from app.models import EmailCaptcha, User

class EmailForms(wtforms.Form):
    email=wtforms.StringField(label="邮箱", validators=[wtforms.validators.Email(message="邮箱格式不正确")])



