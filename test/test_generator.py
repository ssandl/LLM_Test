import pytest
import pymysql
import os
from src.generator import generate_sql

@pytest.fixture(scope="module")
def db_connection():
    conn = pymysql.connect(
            host=os.environ["HOST"],
            port=int(os.environ["PORT"]),
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWD"],
            database=os.environ["DB"],
            charset=os.environ["CHARSET"]
        )
    yield conn
    conn.close()

@pytest.mark.parametrize("table_schema",[
    """
    CREATE TABLE users (
        id INT PRIMARY KEY,
        name VARCHAR(50),
        email VARCHAR(100),
        created_at DATETIME
    );
    """
])
def test_sql_size(db_connection, table_schema):
    sqls = generate_sql(table_schema)
    assert len(sqls) == 10
    
    for sql in sqls:
        with db_connection.cursor() as cursor:
            cursor.execute(sql)
            print(f'sql execute successs:{sql}')