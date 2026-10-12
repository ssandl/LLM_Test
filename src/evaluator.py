import re
import json


def caculate_pass_rate(data: json) -> float:
    """计算通过率

    Args:
        results: sqls执行的结果列表
        data: 汇总的信息，用于生成报告
    
    Returns:
        返回sqls执行结果中的通过率；如果sqls本身是一个空列表，则返回0
    """
    passed = sum(1 for d in data['details'] if d["status"] == "PASS")
    total = data['total']
    data['passed'] = passed
    pass_rate = passed/total if total != 0 else 0
    data['pass_rate'] = pass_rate

fixed_features = {"WHERE": "WHERE", "GROUP_BY": "GROUP BY", "ORDER_BY": "ORDER BY", "JOIN": "JOIN",
                   "LIMIT": "LIMIT", "AGGREGATE": r"\b(COUNT|SUM|AVG|MAX|MIN)\s*\(", "LIKE": "LIKE", 
                   "NULL_CHECK": r"(IS NULL|IS NOT NULL)", "SUBQUERY": r"(IN \(|EXISTS)", 
                   "QUERY": r"(SELECT|INSERT|UPDATE|DELETE)"}

def extract_one_sql_features(info: dict) -> set:
    """获取单个sql中包含的SQL特征
    Args:
        info: data['details']是列表中的元素（字典）

    Returns: 
        返回这个sql中有多少特征的集合
    """
    sql = info["sql"].upper()
    features = set()
    for k, v in fixed_features.items():
        if re.search(v, sql):
            features.add(k)
    info['features'] = features
    return features

def extract_sqls_features(data: json):
    """获取多个sql列表的每个sql特征集合的列表"""
    result_set = set()
    for info in data['details']:
        sql_features = extract_one_sql_features(info)
        result_set = result_set.union(sql_features)
    data['covered_dimensions'] = result_set

def calculate_coverage(data: json):
    extract_sqls_features(data)
    coverage = len(data['covered_dimensions']) / len(fixed_features)
    data['coverage_rate'] = coverage
    data['total_dimension'] = len(fixed_features)