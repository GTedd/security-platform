from app.maintenance.error import LogWriter
from .form import NmapForms
from app.models import Nmap, db
import subprocess
import xmltodict
import json

def scan(request_form):
    form = NmapForms(request_form)
    if form.validate():
        # 获取扫描参数
        arg = parameter(form.mode.data)
        
        # 执行 nmap 扫描
        result = run_nmap(form.ip.data, arg)
        
        # 将扫描结果保存到数据库
        save_scan(form.ip.data, result)
        return result  # 返回的是字典格式的 JSON 对象

def parameter(mode):
    mode_parameter = {
        'found': '-sn',  # 主机发现
        'lite': "-sS",  # 只探测 TCP 开放端口
        # tcp、版本、操作系统、快速扫描
        'default': "-sS -sV -A",
        # -sU:UDP -vv:最详细
        'full': "-sS -sU -sV -O -vv"
    }
    return mode_parameter[mode]

# 使用 subprocess 提权运行 nmap 扫描
def run_nmap(ip, arg):
    try:
        # 使用 -oX 参数指定输出为 XML 格式
        command = ['sudo', 'nmap', '-oX', '-', '-sS', ip] + arg.split()
        
        # 捕获 nmap 执行的输出
        result = subprocess.check_output(command, stderr=subprocess.STDOUT)
        
        # 将 nmap XML 输出转换为 Python 字典
        json_result = xmltodict.parse(result)
        
        # 返回 JSON 对象
        return json_result  # 这是一个 Python 字典（JSON 对象）
    
    except subprocess.CalledProcessError as e:
        LogWriter.error(f'执行 nmap 扫描失败: {e.output.decode("utf-8")}')
        raise

# 将扫描结果保存到数据库
def save_scan(ip, result):
    # 将扫描结果保存到数据库
    json_result = Nmap(ip=ip, result=json.dumps(result))  # 需要将字典转换成字符串存储
    db.session.add(json_result)
    try:
        db.session.commit()
    except Exception as e:
        LogWriter.error('nmap 结果保存数据库失败')
        raise e
    return 'OK'
