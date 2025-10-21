from flask import Blueprint,render_template, request
from app.blueprints.auth.captcha import send_captcha
from .register import register_user

bp = Blueprint('register', __name__,url_prefix='/register')

@bp.route('/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if register_user(request.form)=='failed':
            return "注册失败"
        else:
            return render_template('login.html')
    else:
        return render_template('register.html')

@bp.route('/captcha',methods=['POST'])
def captcha():
    if send_captcha(request.form)=='ok':
        return '发送成功'
    else:
        return '发送失败'

