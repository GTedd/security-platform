from app.models import User, db
from app.maintenance.error import LogWriter
#保存用户
def add_user(username,password,email):
    user = User(username=username, password=password, email=email)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        log=LogWriter()
        log.error("保存用户失败")
        raise '保存用户失败'
    return 'OK'

#删除用户
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    try:
        db.session.commit()
    except Exception:
        log=LogWriter()
        log.error("删除用户失败")
        raise '删除用户失败'
    return 'OK'

#查找用户
def search_user(username):
    user = User.query.filter_by(username=username).first()
    return user

#修改用户信息
def modify_user(username, password, email):
    user = User.query.filter_by(username=username).first()
    user.password = password
    user.email = email
    try:
        db.session.commit()
    except Exception:
        log=LogWriter()
        log.error("修改用户信息失败")
        raise '修改用户信息失败'
    return 'OK'