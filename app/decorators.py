from functools import wraps
from flask import g, redirect, request,url_for
from urllib.parse import urlparse
#装饰器不是很懂
def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            next_path = urlparse(request.url).path
            return redirect(url_for('login.login', next=next_path))
    return inner
