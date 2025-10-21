import subprocess
from .form import DirsearchForm
import json
import time
import shlex
import re

def generate_output(process):
    """生成器函数，用于流式传输命令输出"""
    for line in iter(process.stdout.readline, b''):
        # 将输出行转换为JSON格式
        output_data = {
            "message": line.decode().strip()
        }
        yield f"data: {json.dumps(output_data)}\n\n"

def format_line(line):
    """
    根据不同类型的输出添加相应的颜色样式
    """
    # 处理时间戳和状态码行
    timestamp_pattern = r'\[([\d:]+)\]\s+(\d{3})\s+-\s+(\d+[B])\s+-\s+(.+)'
    timestamp_match = re.match(timestamp_pattern, line)
    if timestamp_match:
        time, status, size, path = timestamp_match.groups()
        status_class = f'status-{status}'
        return (
            f"<span class='timestamp'>[{time}]</span> "
            f"<span class='{status_class}'>{status}</span> - "
            f"<span class='size'>{size}</span> - "
            f"<span class='path'>{path}</span>"
        )

    # 处理进度条行
    progress_pattern = r'(.*errors:\d+)(\[#+\s*\])\s+(\d+%)\s+(\d+/\d+)\s+(\d+/s)\s+(job:\d+/\d+)'
    progress_match = re.match(progress_pattern, line)
    if progress_match:
        info, bar, percent, count, speed, job = progress_match.groups()
        return (
            f"<span class='progress-info'>"
            f"{info} "
            f"<span class='progress-bar'>{bar}</span> "
            f"<span class='progress-percent'>{percent}</span> "
            f"{count} {speed} {job}"
            f"</span>"
        )

    # 其他类型的输出
    if 'Task Completed' in line:
        return f"<span class='complete-info'>{line}</span>"
    elif 'Starting:' in line:
        return f"<span class='start-info'>{line}</span>"
    elif 'Error' in line.lower():
        return f"<span class='error-info'>{line}</span>"
    elif 'WARNING' in line:
        return f"<span class='warning-info'>{line}</span>"
    else:
        return f"<span class='normal-info'>{line}</span>"

def dirsearch(target_url):
    """
    目录扫描函数 - 单个URL扫描，直接流式输出原始数据
    :param target_url: 目标URL
    :yield: 扫描结果
    """
    yield f"Starting directory scan for: {target_url}"
    
    cmd = f'dirsearch -u "{target_url}"'
    
    try:
        process = subprocess.Popen(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        
        # 直接输出原始数据
        for line in process.stdout:
            if line.strip():
                yield line.strip()
        
        process.wait()
        
        if process.returncode != 0:
            error = process.stderr.read()
            yield f"Error occurred: {error}"
            
    except Exception as e:
        yield f"Error executing dirsearch: {str(e)}"
    
    yield "Scan completed!"

def dirsearch_api(request_form):
    form = DirsearchForm(request_form)
    if form.validate():
        # 构建命令
        cmd = [
            "dirsearch",
            "-u", form.url.data,  # 从表单获取URL
            "-t", "100",          # 线程数
            "-R", "2",           # 递归深度
            "-F",                # 完整扫描
            "--format", "json"   # 输出格式为JSON
        ]

        try:
            # 使用 Popen 启动进程，并设置实时输出
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # 合并标准错误到标准输出
                bufsize=1,
                universal_newlines=False
            )

            # 返回 SSE 流式响应
            return Response(
                stream_with_context(generate_output(process)),
                mimetype='text/event-stream'
            )

        except Exception as e:
            return {"error": f"执行出错: {str(e)}"}, 500

    # 如果表单验证失败，返回错误信息
    return {"error": form.errors}, 400