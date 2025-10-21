from app import start
from app.detect_env import environment

#请先看README.md

#检测环境是否可以运行程序
environment() 

#启动Web程序
app=start() 
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
     