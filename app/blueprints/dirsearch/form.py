import wtforms
from wtforms.validators import DataRequired, Regexp, ValidationError

class DirsearchForm(wtforms.Form):
    url = wtforms.StringField(label="目标URL", validators=[
        DataRequired(message='请输入目标URL'),
        Regexp(
            r'^https?:\/\/([\w\d\-]+\.)+[\w\d\-]+(\/.*)?$',
            message="请输入有效的URL，例如 http://example.com"
        )
    ])