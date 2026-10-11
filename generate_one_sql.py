# Please install OpenAI SDK first: `pip3 install openai`
import os
from openai import OpenAI

# print(os.environ.get('DEEPSEEK_API_KEY'))

URL="https://api.deepseek.com"

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url=URL)

# 表结构
table_schema = """
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    created_at DATETIME
);
"""

# 系统要求
SYSTEM_PROMPT = """
你是一个数据库测试专家，擅长根据表结构生成高质量的测试 SQL。
要求：
1. 只返回 SQL 语句，不要任何解释、注释或 Markdown 代码块。
2. SQL 必须语法正确，能在 MySQL 中执行。
3. 覆盖常见查询场景：条件查询、聚合、排序、连接等。
"""


response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"请根据下面的表结构，生成一条测试SQL:\n\n{table_schema}"},
    ],
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}}
)

print(response.choices[0].message.content)
print('-' * 50)
print(response.choices[0].message)