import platform
import pymysql
from .config import *

# 汇总
def environment():
    os()
    mysql()
    


# 操作系统检测
def os():
    print(f'\n当前操作系统:'+platform.system())


# 数据库
def mysql():
    try:
        # 建立连接
        connection = pymysql.connect(
            host=HOSTNAME,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE
        )
        print("\n数据库连接成功\n")
    except pymysql.MySQLError as e:
        # 输出原始错误
        print(f"\n数据库连接失败，请检查数据库是否开启和配置是否正确\n{e}\n")
        # 针对 MySQL 8 认证插件不兼容的提示
        err_msg = str(e)
        if "Authentication plugin" in err_msg or "plugin" in err_msg:
            print("可能是 MySQL 8.0 上的用户认证插件与 PyMySQL 不兼容。")
            print("请登录 MySQL，检查并修改该用户的认证插件：")
            print(f"SELECT user, host, plugin FROM mysql.user WHERE user='{USERNAME}';")
            print(f"ALTER USER '{USERNAME}'@'localhost' IDENTIFIED WITH mysql_native_password BY '{PASSWORD}';")
            print(f"ALTER USER '{USERNAME}'@'%' IDENTIFIED WITH mysql_native_password BY '{PASSWORD}';")
            print("FLUSH PRIVILEGES;")
            print("如果需要使用 caching_sha2_password，请确保启用 SSL 或使用 mysql-connector-python 客户端。")
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()