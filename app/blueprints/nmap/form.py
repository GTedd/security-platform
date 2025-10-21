import wtforms
from wtforms.validators import Regexp
from app.models import Nmap

#nmap验证
class NmapForms(wtforms.Form):
    ip = wtforms.StringField(label="IP地址", validators=[wtforms.validators.IPAddress(message="IP地址格式不正确")])
    mode = wtforms.StringField(label="扫描模式",validators=[Regexp(r'^(found|lite|default|full)$', message="模式错误")])