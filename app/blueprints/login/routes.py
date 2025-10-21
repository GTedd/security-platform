from flask import Blueprint, redirect, render_template, request,url_for
from .login import login_user

bp = Blueprint('login', __name__,url_prefix='/login')

@bp.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if 0==login_user(request.form):
            #没有使用过滤，存在漏洞！跨站脚本攻击
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index.index'))
        else:
            return '登入失败'
    return render_template('login.html')


