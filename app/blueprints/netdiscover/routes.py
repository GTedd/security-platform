from flask import Blueprint,request,render_template
from app.decorators import login_required
from .netdiscover import netdiscover
bp=Blueprint('netdiscover',__name__,url_prefix='/netdiscover')

@bp.route('/',methods=['GET','POST'])
@login_required
def index():
    if request.method == 'POST':
        result=netdiscover(request.form)
        return result
    else:
        return render_template('netdiscover.html')