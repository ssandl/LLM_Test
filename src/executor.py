import pymysql
import os
import json

def db_connect():
    # pymysql默认
    conn = pymysql.connect(
        host=os.environ["HOST"],
        port=int(os.environ["PORT"]),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWD"],
        database=os.environ["DB"],
        charset=os.environ["CHARSET"],
        autocommit=False  # 所有的sql语句（除了DDL）都不会commit，在连接断开时回滚；这样就不会对数据造成影响）
    )
    return conn

def db_close(conn:pymysql.Connection):
    conn.close()

def db_execute_one_sql(conn: pymysql.Connection, sql: str, data: json):
    """执行单条sql语句

    Args:
        conn: 数据库连接
        sql: 待执行的sql语句
        data: 存储所有信息用于生成报告

    Returns: (result, info)
        result: 执行sql的结果，如果为False代表失败，如果为Ture代表成功
        info:   执行失败的错误信息
    """
    result = "PASS"
    error = ""
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
    except pymysql.MySQLError as e:
        result = "FAIL"
        error = str(e)
    return data['details'].append({
        "sql": sql,
        "status": result,
        "error": error
    })

def db_execute_sqls(conn: pymysql.Connection, sqls: list) -> json:
    """执行多条sql语句

    Args:
        conn: 数据库连接
        sqls: 多条sql的列表
    
    Returns:
        所有sql执行后的统计数据的json格式
    """
    data = {}
    data['total'] = len(sqls)
    data['details'] = []
    for sql in sqls:
        db_execute_one_sql(conn, sql, data)
    return data