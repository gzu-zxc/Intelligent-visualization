prompt = """根据给定的机器学习分析任务，根据上下文构建具体的机器学习管道，并按如下格式输出：
{”dataset“: <数据集>, ”task“: <任务类型>, "preprocess": <预处理方法>, 
"feature_engineering": <特征工程方法>, "model": <模型>, "evaluate": <评估方法>}

上下文开始
数据集：iris.csv, housing.csv, zoo.csv, airport.csv, 豆瓣读书评分.csv, 母婴用品销售数据.csv
任务类型：classification, regression, timeseries
预处理方法：continuous, discretize
特征工程方法：impute, select_column
模型：random_forest, tree, linear_regression, svm
评估方法：prediction, matrix_confusion, roc, mse
上下文结束

问：帮我预测一下房价
答：
"""
prompt_simple = """根据给定的机器学习任务，根据上下文信息分析其使用的数据集、任务类型，并按照JSON格式输出，参考：
{dataset: {name: <数据集名称>, target: <待预测的列名>}, task: <任务类型>}

上下文开始
数据集：[
{name: iris, columns: [{name: iris, description: 类别}, {name: sepal_width, description: 萼片宽}, ]},
{name: housing, columns: [{name: p, description: 价格}, {name: ratio, description: 面积}, 
{name: location, description: 位置}, {name: room, description: 房间数}]}
]
任务类型: [classification, regression, timeseries, clustering]
上下文结束

问：预测房价
答：
"""
print(prompt_simple)

q_list = [
    "预测鸢尾花的类别",
    "预测房价",
]

