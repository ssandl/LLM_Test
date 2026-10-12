from src.generator import generate_sql
from src.executor import db_connect, db_close, db_execute_sqls
from src.evaluator import caculate_pass_rate, calculate_coverage, extract_sqls_features, fixed_features
import json

# 表结构
table_schema = """
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    created_at DATETIME
);
"""

def make_reporter(data):
    print(f'当前的sql数量：{len(data['details'])}。')
    print(f'通过率：{data['pass_rate']:.2%}，覆盖率：{data['coverage_rate']:.2%}')
    print('-' * 100)
    print('通过率/覆盖率详情：')
    for info in data['details']:
        print(
            f'通过情况：{"通过" if info['status'] == 'PASS' else "不通过":<8}，' 
            f'覆盖特征：{str(info['features']):<50}, sql语句：{info['sql']}'
        )

try:
    sqls = generate_sql(table_schema)
    conn = db_connect()
    data = db_execute_sqls(conn, sqls)
finally:
    db_close(conn)

caculate_pass_rate(data)
calculate_coverage(data)
make_reporter(data)

