from flask import session
from .form import RegisterForms
from app.blueprints.auth.user import add_user

def register_user(request_form):
    form=RegisterForms(request_form)
    if form.validate():#验证表单是否有效
        #写入数据库
        session['user_id']=form.username.data#创建session会话以供下次免登入
        add_user(form.username.data,form.password.data,form.email.data)
        return 'OK'
    else:
        return 'failed'




