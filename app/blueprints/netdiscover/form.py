import wtforms
from wtforms.validators import DataRequired, Regexp, ValidationError

class NetdiscoverForm(wtforms.Form):
    time = wtforms.StringField(label="扫描时间",validators=[DataRequired(message='请输入扫描时间'),
            Regexp(r"^\d+$", message="请输入有效的整数")
        ])
    range = wtforms.StringField(label="IP地址",validators=[DataRequired(message='请输入 IP 地址'),
            Regexp(
                r"^(?:\d{1,3}\.){3}\d{1,3}/(?:[0-9]|[1-2][0-9]|3[0-2])$",
                message="请输入有效的 IP 范围，例如 192.168.1.0/24"
            )
        ]
    )

    def validate_time(self, field):
        if field.data:
            try:
                value = int(field.data)
                if not (1 <= value <= 60):
                    raise ValidationError("请输入 1 到 60 之间的秒数")
            except ValueError:
                raise ValidationError("请输入有效的整数")
        else:
            raise ValidationError("请输入扫描时间")
