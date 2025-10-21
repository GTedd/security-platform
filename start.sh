#!/bin/bash

# 设置缓存目录
export PYTHONPYCACHEPREFIX="${PWD}/_pycache"

# 创建缓存目录（如果不存在）
mkdir -p "$PYTHONPYCACHEPREFIX"

# 启动 Python 脚本
python start.py
