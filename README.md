* 注:本项目从gitee迁移至github平台，负责人已发生变动，后续开发将在此完成

# 御网智卫——基于深度感知的安防平台
## 一、项目介绍
### 1、简述
本项目是一个Web网络安全监护平台，提供各种安全和检测工具，特点是易于上手，为各类非网络安全专业的人员提供一定量的安全监控服务  
## 二、项目结构
### 1、语言
本项目使用的开发语言是python,特点是容易上手，并且python内集成内各类工具，容易集成，以便各类二次开发  
### 2、框架
本项目是使用flask框架作为基本web框架，使用蓝图作为模块，一个蓝图对应一个模块，最后在一个文件汇总  
### 3、项目树状结构
/security-platform  
│  
├── app/                        # 主应用目录  
│   ├── __init__.py             # 初始化应用，注册蓝图和配置，汇总  
│   ├── config.py               # 配置文件（拓展功能的配置）  
│   ├── extensions.py           # 扩展功能 (数据库、邮箱等)  
│   ├── models.py               # 数据库模型  
│   ├── decorators.py           # 装饰器，用于验证是否已登入  
│   ├── detect_env.py           # 环境检测，用于在启动前检测各类环境是是否配备起全(mysql等)  
│   │  
│   ├── blueprints/             # 蓝图模块，每各模块都放在里面  
│   │   ├── auth/               # 授权模块，用于各种验证和授权的功能  
│   │   │   ├──captcha.py       # 验证码功能实现  
│   │   │   ├──forms.py         # 表单功能实现  
│   │   │   └──user.py          # 用户数据库操作  
│   │   │  
│   │   ├── dirsearch           # dirsearch模块  
│   │   │  
│   │   ├── index/              # 主页显示  
│   │   │   ├──index.py         # 主页代码实现  
│   │   │   └──routes.py        # 主页导航访问实现  
│   │   │  
│   │   ├── login/              # 登入页面模块  
│   │   │  
│   │   ├── nmap/               # nmap模块  
│   │   │  
│   │   ├── netdiscover/        # netdiscover模块  
│   │   │  
│   │   └── register/           # 注册页面模块  
│   │  
│   ├── maintenance/            # 日志维护类  
│   │   ├── logs/               # 日志文件夹  
│   │   │   │ 
│   │   │   └──error.log        # 报错日志  
│   │   │  
│   │   └── error.py            # 报错写入  
│   │  
│   ├── static/                 # 存放静态资源  
│   │  
│   ├── templates/              # 网页html渲染模板  
│   │   ├──dirsearch.html       # dirsearch功能页面模板  
│   │   ├── index.html          # 主页模板  
│   │   ├── login.html          # 登录页面模板  
│   │   ├── nmap.html           # nmap功能页面模板  
│   │   ├── netdiscover.html    # netdiscover功能页面模板  
│   │   └── register.html       # 注册页面模板  
│   │  
│   └── utilities/              # 软件工具存放 (如 sqlmap的可执行文件)  
│  
├── requirements.txt            # 项目依赖  
│  
├── start.py                    # 启动项目的主脚本  
│  
└── start.sh                    # shell启动脚本，可以设置环境变量(如修改框架缓存文件)  
## 三、部署说明
### 1、环境安装
本项目需要准备python3的环境  
安装下列python依赖库:  
flask
flask_SQLAlchemy
flask_migrate
pymysql
flask_mail
wtforms
email_validator
python-nmap
xmltodict
dirsearch
setuptools 
  
`pip install -r requirements.txt`可以一键安装依赖  
建议使用虚拟环境安装python依赖：`python -m venv .venv`
### 2、数据库准备
在app/config内有连接数据库的配置，需要将其修改成自己的用户名和密码  
还需要在你的mysel内建立security的数据库CREATE DATABASE security;  
完成之后在根目录使用下列命令建表(数据库模型)  
`flask --app start db init`  
`flask --app start db migrate -m "迁移数据库"`  
`flask --app start db upgrade`  
### 3、启动应用
直接使用python运行security-platform下的start.py  
`python start.py`  
linux推荐使用./start.sh启动  
### 4、Windows启动
待定，可能不会做，因为有点工具是linux独有的，跨平台比较麻烦  
### 5、docker启动  
待定  
## 四、开发说明
### 1、程序启动步骤说明
#### (1)、start.py
应用从start.py开始启动整个项目，一开始先会进行一系列的环境和配置的检查，确保可以正确启动，完成检查后会启动并进入__init__.py的start()函数  
#### (2)、__init__.py
程序先创建一个flask框架，然后把必要的配置文件导入给flask，接着初始化数据库和邮箱模块，完成之后就可以执行使用数据库迁移，以便添加和更新数据库的表(模型)  
#### (3)、extension.py
里面存放的是一些需要在初始化的时候就要传入flask框架的模块，主要有数据库db和邮箱mail模块  
#### (4)、config.py
这个文件主要是给extension.py存放配置信息用的，因为通常放在extension.py的模块都是需要比较多的配置信息，单独分离出来可以方便管理全部配置信息  
记住：config.py是给extension.py服务的  
#### (5)、models.py
数据库模型描述了security数据库内有什么数据表(模型)，一个类为一个模型(一张表)，表的内部描述了这张表内有什么字段，类型是什么。如果要写入数据库或者建立新的表在这里添加/修改  
#### (6)、Migrate()
用于数据库迁移使用，一般来说只有首次或者更新数据库模型的时候会执行这个类，用于将模型写入到数据库内部或者更新现有数据库，这样做得好处是不需要手动输入sql语句来创建数据表，有助于在不同机器上部署的时候可以快速建立数据库能够满足项目的预设格式  
对应 三、部署说明->2、数据库准备内的命令  
`flask --app start db init`
`flask --app start db migrate -m "迁移数据库"`
`flask --app start db upgrade`
#### (7)、blueprints()
这里对应下面的blueprints()函数，主要是加载应用模块的区域，一个蓝图对应一个模块，如果想添加新的模块只要在blueprints()函数内导入该模块包，并且在后面添加上app.register_blueprint(模块)就可以加载模块，导包和加载模块是成对存在的  
### 2、文件夹blueprints
这个文件夹主要是存放模块的后端处理代码，一个文件夹对应一个模块，对于需要在网页上加载的模块，内部会存在2个文件：模块.py和routes.py  
#### (1)、routes.py
routes.py只有三个作用：  
1. 将蓝图传给flask框架，以便在__init__.py的blueprints()内选择是否加载该模块  
2. 让网页可以通过url访问到该模块  
3. 导入 模块.py,将全部后端的业务代码交给 模块的py来处理，最后将接过返回给前端  
#### (2)、模块.py
存放该模块全部的业务代码的实现，可以有多个文件，只要做到能够处理完成后将结果传给routes.py并让其返回给前端即可  
### 3、文件夹static
主要是存放前端需要使用的静态资源，如：图片、js、css代码  
### 4、utilities
存放外部调用的工具二进制文件或者源码，以供每一个模块调用这里的工具，便于直接项目迁移的时候可以直接将工具带走  
### 5、文件夹migrations
数据库初始化默认生成的文件夹，不需要动，只有在输入(6)、Migrate()的三条命令时候会用到它，可以选择删除掉，只不过在下次想要添加/更新数据模型的时候需要重新生成  
### 6、表单的使用
每个模块内的forms.py是用来验证表单的，如果需要在前端在处理接受的数据之前，请先使用forms.py内的wtforms模块创建一个表单验证类，就不需要自己写验证函数来验证了  
### 7、用户验证模块
使用一个装饰器decorators.py验证是否登入了，如果没有登入则会要求先登入在进行访问，只需在每一个模块的route.py文件@bp.route()下方添加@login_required即可实现自动验证登入跳转  
### 8、maintenance文件夹
一般是用来保存并写入日志的，里面的logs是存放日志的目录，error.py可以调用内部的方法来写入错误日志  
## 五、其他
