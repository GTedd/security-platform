import email
from wsgiref import validate
from flask import redirect, request, session
from .form import LoginForms
from app.models import User

def login_user(request_form):
    form=LoginForms(request_form)
    if form.validate():
        user=User.query.filter_by(email=form.email.data).first()
        session['user_id']=user.username
        return 0
    else:
        return -1