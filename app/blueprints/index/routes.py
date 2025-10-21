from flask import Blueprint, render_template
bp = Blueprint('index', __name__,url_prefix='/')

@bp.route('/index')
def home():
    return render_template('index.html')

@bp.route('/')
def index():
    return render_template('index.html')