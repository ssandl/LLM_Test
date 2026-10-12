import os
import json
from openai import OpenAI

# 系统要求
SYSTEM_PROMPT = """
你是一个数据库测试专家，擅长根据表结构生成高质量的测试 SQL。
要求：
1. 只返回 SQL 语句，不要任何解释、注释或 Markdown 代码块。
2. SQL 必须语法正确，能在 MySQL 中执行。
3. 覆盖常见查询场景：条件查询、聚合、排序、连接等。
4. 严格使用json的格式返回所有的SQL语句。
示例输入: 
请根据下面的表结构，生成2条测试SQL:
    CREATE TABLE users (
        id INT PRIMARY KEY,
        name VARCHAR(50),
        email VARCHAR(100),
        created_at DATETIME
    );

示例JSON输出:
{
    "sql": ["SELECT * FROM users;", "SELECT id, name, email, created_at FROM users WHERE name = 'Alice';"]
}
"""

output_sql_size = 10

def generate_sql(table_schema):
    URL="https://api.deepseek.com"

    client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url=URL)

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"请根据下面的表结构，生成{output_sql_size}条测试SQL:\n\n{table_schema}"},
        ],
        response_format={'type': 'json_object'},
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # print(response.choices[0].message.content)
    # print('-' * 50)
    # print(response.choices[0].message)
    results = json.loads(response.choices[0].message.content)
    if "sql" in results:
        return results["sql"]
    return []

if __name__ == '__main__':
    # 表结构
    table_schema = """
    CREATE TABLE users (
        id INT PRIMARY KEY,
        name VARCHAR(50),
        email VARCHAR(100),
        created_at DATETIME
    );
    """
    sqls = generate_sql(table_schema)
    print(len(sqls))
    print(sqls)