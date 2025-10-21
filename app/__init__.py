from flask import Flask, session,g
from app import config
from app.extensions import db,mail
from app.models import User
from flask_migrate import Migrate

def start():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    mail.init_app(app)
    Migrate(app, db)
    before_request_hook(app)
    blueprints(app)
    return app

def blueprints(app):
    from .blueprints.index.routes import bp as index_bp
    from .blueprints.login.routes import bp as login_bp
    from .blueprints.register.routes import bp as register_bp
    from .blueprints.nmap.routes import bp as nmap_bp
    from .blueprints.netdiscover.routes import bp as netdiscover_bp
    from .blueprints.dirsearch.routes import bp as dirsearch_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(nmap_bp)
    app.register_blueprint(netdiscover_bp)
    app.register_blueprint(dirsearch_bp)


def before_request_hook(app):
    #HOOK钩子函数
    #全局验证是否登入
    @app.before_request
    def before_request():
        user_id=session.get('user_id')
        if user_id:
            setattr(g,'user',user_id)
        else:
            setattr(g, 'user', None)
    
    #不是很清楚如何分类
    #上下文处理器
    @app.context_processor
    def context_processor():
        return {"user": g.user}