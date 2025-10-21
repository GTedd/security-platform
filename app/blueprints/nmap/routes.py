from flask import Blueprint, render_template, request
from .my_nmap import scan
from app.decorators import login_required
bp = Blueprint('nmap', __name__,url_prefix='/nmap')

@bp.route('/',methods=['GET','POST'])
@login_required#必须登入后才可以使用它
def index():
    if request.method == 'POST':
        return scan(request.form)
    return render_template('nmap.html')
