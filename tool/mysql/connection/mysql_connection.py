import mysql.connector
import pymysql

def getConnection():
    connection = pymysql.connect(
        host='localhost',  # 数据库主机地址
        port=3306,  # 端口号，默认 3306
        database='sale_management',  # 数据库名
        user='root',  # 用户名
        password='123456',  # 密码
        # --- 关键：使用 cursorclass (无下划线) ---
        # 并指定 PyMySQL 自带的 DictCursor
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection

if __name__ == '__main__':
    getConnection()