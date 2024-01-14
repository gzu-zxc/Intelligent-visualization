import json
import random
from vis.chart_config import ALL_CHARTS


def mock_dataset(chart_name):
    """为名称时 chart_name 的 chart 生成对应的 mock 数据"""
    if chart_name not in ALL_CHARTS:
        supported_chart = ",".join(ALL_CHARTS.keys())
        raise Exception(f"{chart_name} 不存在， 系统支持的 chart 列表：{supported_chart}")
    with open("vis/test/data.json", "r", encoding="utf-8") as f:
        mock_prompt = json.load(f)
    with open("vis/test/table.json", "r", encoding="utf-8") as f:
        mock_table = json.load(f)

    instruction = mock_prompt[chart_name]["prompt"][random.randint(0, len(mock_prompt[chart_name]["prompt"]))-1]
    dataset_field_list = []
    tableList = mock_prompt[chart_name]["tableList"]
    for item in tableList:
        table_name = item["dataTable"]
        table_config = dict(dataTable=table_name, fieldList=[])
        alias_list = item["alias"]
        # 根据列的alias，从table里面获取所有列的原始配置
        for alias in alias_list:
            for field in mock_table["field"]:
                if table_name == field["dataTable"]:
                    for item in field["fieldList"]:
                        if item["alias"] == alias:
                            table_config["fieldList"].append(item)
                            break
        dataset_field_list.append(table_config)
    return {
        "instruction": instruction,
        "history": [],
        "dataset": {"field": dataset_field_list}
    }