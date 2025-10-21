from flask_mail import Message
from app.extensions import mail,db
import random
from app.models import EmailCaptcha
from app.blueprints.auth.forms import EmailForms, email
from app.maintenance.error import LogWriter

def send_captcha(recive_email):
    form=EmailForms(recive_email)
    if form.validate():#验证表单是否有效
        captcha = generate_captcha()
        email=form.email.data
        msg = Message('安全验证码', recipients=[email])
        msg.body = '您的验证码为：'+captcha
        try:
            #发送验证码
            mail.send(msg)
        except Exception as e:
            log=LogWriter()
            log.info('发送验证码失败')
            raise e
        #保存验证码到数据库
        save_captcha(email,captcha)
        return 'ok'
    

    #生成验证码
def generate_captcha():
    code = ""
    for _ in range(4):
        code += str(random.randint(0, 9))
    return code

def save_captcha(email,captcha):
    #这里要小写转换
    email_code = EmailCaptcha(email=email, captcha=captcha)
    db.session.add(email_code)
    try:
        db.session.commit()
    except Exception as e:
        log=LogWriter()
        log.error('保存验证码失败')
        raise Exception('保存验证码失败') 
    return 'OK'