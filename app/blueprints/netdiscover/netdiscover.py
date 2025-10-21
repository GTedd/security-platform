import subprocess
import threading

from app.maintenance.error import LogWriter
from .form import NetdiscoverForm


def netdiscover(request_form):
    form = NetdiscoverForm(request_form)
    if form.validate():
        raw = run_netdiscover(
            form.range.data, int(form.time.data)
        )  # 原始数据需要进行处理变成json数据
        if raw:
            # 数据去重
            unique_devices = parse_netdiscover_output(raw)
            return unique_devices

# 通过使用子进程调用外部命令
def run_netdiscover(range, timeout=5):
    try:
        # 启动 netdiscover 进程
        process = subprocess.Popen(
            # 主要修改这里的网卡
            ["sudo", "netdiscover", "-i", "ens18", "-r", range],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # 使用计时器在 timeout(默认5) 秒后终止进程
        timer = threading.Timer(timeout, process.terminate)
        timer.start()

        # 获取输出
        stdout, stderr = process.communicate() 

        # 取消计时器
        timer.cancel()
        return stdout
    except Exception as e:
        LogWriter.error('netdiscover出现问题')
        raise 'netdiscover出现问题'

# 数据处理
def parse_netdiscover_output(output):
    devices = set()
    for line in output.splitlines():
        if line.strip() and not any(
            keyword in line for keyword in ["Currently", "IP", "Packets"]
        ):
            parts = line.split()
            if len(parts) >= 2:
                ip = parts[0]
                mac = parts[1]
                if validate_ip(ip) and validate_mac(mac):
                    devices.add((ip, mac))
    return [{"IP": ip, "MAC": mac} for ip, mac in devices]


def validate_ip(ip):
    parts = ip.split(".")
    return len(parts) == 4 and all(
        part.isdigit() and 0 <= int(part) <= 255 for part in parts
    )


def validate_mac(mac):
    return len(mac.split(":")) == 6
