from flask import Blueprint,request,render_template
from app.decorators import login_required
from .template import template
bp=Blueprint('template',__name__,url_prefix='/template')

@bp.route('/',methods=['GET','POST'])
@login_required
def index():
    if request.method == 'POST':
        template()
    return render_template('template.html')