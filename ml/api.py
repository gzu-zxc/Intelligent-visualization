import os
import json

available_apis = [
    dict(domain="数据读写", functionality="", api_name="io",
         api_call="io.aistudio", api_arguments={},
         performance=None, description=None),
    dict(domain="机器学习模型", functionality="", api_name="model",
         api_call="model.aistudio", api_arguments=None,
         performance=None, description=None),
    dict(domain="聚类算法", framework=None, functionality=None, api_name="clustering",
         api_call="clustering.aistudio", api_arguments={},
         performance=None, description=None),
    dict(domain="特征工程", functionality="", api_name="feature-engineering",
         api_call="feature-engineering.aistudio", api_arguments={},
         performance=None, description=None),
    dict(domain="数据预处理", functionality="", api_name="preprocess",
         api_call="preprocess.aistudio", api_arguments={},
         performance=None, description=None),
    dict(domain="模型评估", functionality="", api_name="evaluate",
         api_call="evaluate.aistudio", api_arguments={},
         performance=None, description=None),
    dict(domain="可视化", functionality="", api_name="visualize",
         api_call="visualize.aistudio", api_arguments={},
         performance=None, description=None),
]

api_str = "\n".join([json.dumps(item, ensure_ascii=False) for item in available_apis])

prompt = f"""根据给定任务，构建一个机器学习管道，按调用顺序返回一个API调用列表

使用如下APIs：
{api_str}
使用如下数据集：
iris, housing, airport, zoo, wine

按照如下流程进行处理
1. 数据加载
2. 数据预处理 
3. 特征工程
4. 模型训练
5. 模型评估

参考如下案例：
用户：对鸢尾花数据集进行分类
助理：
1. 首先加载数据集
{{"api_call": "io.aistudio", functionality: "file", "api_arguments": {{"file_name": "iris.csv"}}}}
2. 然后对数据进行预处理
{{"api_call": "feature-engineering.aistudio",  functionality: "continuous", "api_arguments": None}}
{{"api_call": "preprocess.aistudio",  functionality: "impute", "api_arguments": None}}
3. 构建模型
{{"api_call": "model.aistudio",  functionality: "random forest", "api_arguments": None}}
4. 评估模型
{{"api_call": "evaluate.aistudio",  functionality: "prediction", "api_arguments": None}}
"""
task_list = [
    ("对鸢尾花数据集进行分类", ""),
    ("帮我预测一下房价", ),
]
