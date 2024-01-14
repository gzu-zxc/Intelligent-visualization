# 与 vis/assets/subtask.txt 保持一致
with open(r"vis/assets/subtask.txt", encoding="utf-8") as f:
    subtask = f.read()

# dataset_info（vis.dataset.Dataset）
# ## 数据集
# 表：sale (发货日期,行ID,订单ID,订单日期,快递方式,客户ID,客户名称,细分,城市,省自治区,国家,地区,产品ID,类别,子类别,产品名称,销售额,数量,折扣,利润)

# 与 vis/assets/chart.txt 保持一致
with open(r"vis/assets/chart.txt", encoding="utf-8") as f:
    context_info = f.read()

with open(r"vis/assets/sample.txt", encoding="utf-8") as f:
    sample_info = f.read()

prompt_template = """你是一个可视化分析师，你的主要职责是将用户的可视化需求分解为多个子任务，并将其转换为一系列可视化分析系统可识别的JSON格式化信息返回给系统展示,使用尖括号<>来说明字段中的信息，不表示取值。
{subtask}
{context_info}
{sample_info}
{dataset_info}
{instruction}
"""

q_list = [
    "可视化分析任务：各个细分产品在各个城市的销售额占比是多少？",
    "我想看不同地区的各个细分产品的销售额，使用BarStack"
]
intention_analysis_prompt_template = """你是一个可视化分析师，你的主要职责是对用户查询进行意图分析，执行每个子任务。
当完成所有子任务后，最后将其转换为一系列可视化分析系统可识别的JSON格式化信息返回给系统展示,使用尖括号<>来说明字段中的信息，不表示取值。

## 意图分析子任务
1. 分析用户查询意图
2. 输出JSON格式的结果

{dataset_info}

## 意图
- unreadable: 用户输入了不可读的内容
- meaningless: 用户输入了与当前数据可视化场景无关的无意义的内容
- gen_chart: 生成图表
- recommend_q: 针对系统中的数据信息和可用图表，向用户推荐 3-5 个问题，当用户不知道如何提问、如何分析时，帮助用户进行有意义、有价值的可视化探索
- gen_dashboard: 生成仪表盘
- gen_hue: 生成配色

## 用户查询
{instruction}

## 响应结果格式
{{intention": "<意图>", "response": "<你的回答>"}}
"""

rag_intention_analysis_prompt_template = """你是一个可视化分析师，你的主要职责是对用户查询进行意图分析，同时执行每个子任务并输出相应的中间结果。
在分析的过程中你可以提问，以获取用于完成任务所需的信息。
当完成所有子任务后，最后将其转换为一系列可视化分析系统可识别的JSON格式化信息返回给系统展示,使用尖括号<>来说明字段中的信息，不表示取值。

## 意图分析子任务
1. 分析用户查询意图
2. 改写用户查询，转换为更为清晰、无歧义的表述形式
3. 按照<响应结果格式>输出结果

{dataset_info}

## 用户查询
{instruction}

## 响应结果格式
{{"intention": "<意图>", "revised": "<改写后的用户查询>", "response": {{"type": "<响应类型>", "content": "<响应内容>"}}}}
"""

rag_prompt_template = """你是一个可视化分析师，你的主要职责是将用户的可视化需求分解为多个子任务，同时执行每个子任务并输出相应的中间结果。
在分析的过程中你可以提问，以获取用于完成任务所需的信息。
当完成所有子任务后，最后将其转换为一系列可视化分析系统可识别的JSON格式化信息返回给系统展示,使用尖括号<>来说明字段中的信息，不表示取值。
{dataset_info}

{sample_info}

{instruction}
"""

#################### 生成数据 （测试用）#################################
gen_dataset_prompt = """设计一个数据库模式，基于该数据库模式生成的数据可以用来绘制多种图形，包括：bar, line, pie, doughnut。
对于数据库模式需要满足以下约束：
- 内容与电脑产品销售相关
- 包含2个以上的表

将结果按如下格式返回：
{
  "schema": [
    {
      "name": "<模式名称>",
      "table": [
        {
          "name": "<表名>",
          "attribute": [
            {
              "name": "<列名>",
              "pk": true,
              "fk": false,       
              "type": "<列类型>",
              "description": "<列描述>"
            }
          ]
        }
      ]
    }
  ]
}
"""

gen_recommend_q_prompt = """你是一个可视化分析师，你的主要职责是当用户不知道如何提问、如何分析时，基于提供的数据库模式和可用的图表，设计 {n} 个问题作为用户提示，帮助用户进行有意义、有价值的可视化探索。
## 数据库模式
{dataset}

## 可用的 chart 列表
- pie, 饼图
- doughnut, 环状饼图
- BarStack, 堆叠条
- BarHoriz, 柱状图
- Circle, 圆视图
- DimArea, 面积图（离散）
- DimLine, 折线图（离散）
- FilledMaps, 填充地图
- Maps, 符号地图
- IndicatorCard, 指标卡
- Pies, 饼图
- WordCloud, 词云图
- Table, 表格
- Radar, 雷达图
- PivotTable, 交叉表
- Funnel, 漏斗图
- RectangularTree, 矩形树图

将结果按如下格式返回：
{{"q_list": ["<用户提示>"]}}
"""

gen_recommend_chart_prompt = """针对提供的数据库模式、用户问题、可用的图表，请推荐{n}个图表，并按照推荐程度降序排序。
## 数据库模式
{dataset}
## 用户问题
{instruction}
## 可用的图表
{chart_list}
将结果按如下格式返回：
{{"chart_list": ["<chart>"]}}
"""




