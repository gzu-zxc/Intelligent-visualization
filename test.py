import openai
openai.api_key = "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"  # 公司

import uvicorn
from autollm import AutoFastAPI
from autollm import AutoQueryEngine, read_files_as_documents

documents = read_files_as_documents(input_dir="e:/learning/test/data/")
query_engine = AutoQueryEngine.from_parameters(documents)
# response = query_engine.query("sale数据集有哪些信息？")
prompt = """
你是一个可视化分析师，你的主要职责是将用户的可视化需求分解为多个子任务，并将其转换为一系列可视化分析系统可识别的JSON格式化信息返回给系统展示,使用尖括号<>来说明字段中的信息，不表示取值。
## 样例
各个细分产品在各个地区的销量如何？
### 结果
{"table": "<表名>", "target": ["数量"], "role": "measure", "group_by": ["细分"], "aggregation": "SUM", "chart": "BarHoriz", "geo_role": null, "date_split": "", "order_by": null, "filter": [{"field":null,"type":"useAll"}],"refline": [{"type": null}]}

<<user_query>>
"""
prompt.replace("<<user_query>>", "所有地区的销售额是多少？")
response = query_engine.query(prompt)
if "\n" in response.response:
    for line in response.response.split("\n"):
        print(line)
else:
    print(response.response)

app = AutoFastAPI.from_query_engine(query_engine)
uvicorn.run(app, host="0.0.0.0", port=9000)