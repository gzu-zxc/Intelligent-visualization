import json
import time
import traceback
from autollm import AutoQueryEngine, read_files_as_documents

from flask import Flask
from flask import request

from vis.chat import Chat2X
from vis.mock import mock_dataset
from utils.logging import file_handler, console_handler


# 配置是否使用 autollm 中的查询引擎
use_rag = False
if use_rag:
    documents = read_files_as_documents(input_dir="vis/assets/")
    query_engine = AutoQueryEngine.from_parameters(documents)
else:
    query_engine = None

app = Flask(__name__)

def get_millisecond():
    millis = int(round(time.time()*1000))
    return millis

@app.route("/ai-assistant/va", methods=["POST"])
def va_config():
    """
    Args
        postdata: {
        "instruction": "XXX 在全国的销量如何？",     // 用户请求的问题
        "history": [],        // 待定, 默认值： []
        "dataset": {    //   数据集元信息，是否涉及调用 Uniplore 服务接口获取信息？
            "field": [
                {
                     "dataTable": "student_score",
                     "fieldList": [{
                            "attribute": "name",
                            "alias": "姓名",
                            "type": "dim",
                            "subType": null,
                            "operation": "a8az8nx5xr3p6j7a75zrynab",    // hash
                            "dateSplit": "",
                            "aggregation": "COUNT",
                            "dataTable": "student_score",
                            "isVisible": true,
                            "filter": null,
                            "orderBy": null,
                            "groupBy": "groupby",
                            "calculationBasis": null,
                            "visualRole": null,
                            "visualDatatype": null,
                            "visualType": null,
                            "dataType": "TEXT",
                     }, ...], // fieldList
              }],
              "userDefinedField": [...]
        }, ...}
    :return:
    """
    json_dict = request.json or {}
    form_dict = request.form
    post_data = {**json_dict, **form_dict}

    try:
        instruction = post_data["instruction"]
        history = post_data["history"]  # [{role: user, content: xxx, timestamp: xxx}]
        dataset = post_data["dataset"]

        c2c = Chat2X(instruction=instruction, dataset=dataset, use_rag=use_rag,
                     query_engine=query_engine, history=history)
        # # 1. 意图分析
        # res = c2c.intention_analysis()
        # intention = res["intention"]
        # if intention == "gen_chart":
        #     config = c2c.to_config()
        #     app.logger.info(
        #         f"\n------------------ Chart Config ------------------\n{json.dumps(config, ensure_ascii=False)}")
        #     response = dict(code=200, msg="操作成功", data=config, time=get_millisecond(), total=0)
        # elif intention == "unreadable":
        #     msg = res["response"]
        #     response = dict(code=201, msg=msg, data={}, time=get_millisecond(), total=0)
        # elif intention == "meaningless":
        #     msg = res["response"]
        #     response = dict(code=202, msg=msg, data={}, time=get_millisecond(), total=0)
        # elif intention == "recommend_q":
        #     q_list = c2c.to_q_list(n=3)
        #     response = dict(code=210, msg="操作成功", data={"q_list": q_list}, time=get_millisecond(), total=0)
        # elif intention == "gen_dashboard":
        #     response = dict(code=211, msg="操作成功", data={}, time=get_millisecond(), total=0)
        # else:
        #     response = dict(code=2000, msg="无法识别用户意图", data={}, time=get_millisecond(), total=0)
        config = c2c.to_config()
        # 通过调用 c2c.to_config() 方法生成数据可视化配置。这一过程可能涉及与聊天模型的交互、意图分析和配置生成
        app.logger.info(
            f"\n------------------ Chart Config ------------------\n{json.dumps(config, ensure_ascii=False)}")
        response = dict(code=200, msg="操作成功", data=config, time=get_millisecond(), total=0)
    except Exception as e:
        response = dict(code=2000, msg=str(traceback.format_exc()), data={}, time=get_millisecond(), total=0)
    return response


@app.route("/ai-assistant/va/recommend-q", methods=["POST"])
def recommend_q():
    """根据数据集信息，向GPT询问生成与数据集相关的问题，帮助用户进行有意义、有价值的可视化探索
    Args
        postdata: {
            "n": <生成的提示的个数>,
            "dataset": {},  // 格式与【/ai-assistant/va】中保持一致
       }
    Return
    """
    json_dict = request.json or {}
    form_dict = request.form
    post_data = {**json_dict, **form_dict}
    try:
        dataset = post_data["dataset"]
        n = post_data["n"]
        c2x = Chat2X(instruction="", dataset=dataset, use_rag=use_rag, query_engine=query_engine)
        q_list = c2x.to_q_list(n=n)
        # 通过调用 c2x.to_q_list(n) 方法生成问题列表。这个方法将根据数据集的具体情况，生成 n 个相关的问题，这些问题可以用作绘制图表的提示。
        result = dict(q_list=q_list)
        response = dict(code=200, msg="操作成功", data=result, time=get_millisecond(), total=0)
    except Exception as e:
        response = dict(code=2000, msg=str(traceback.format_exc()), data={}, time=get_millisecond(), total=0)
    return response

@app.route("/ai-assistant/va/recommend-chart", methods=["POST"])
def recommend_chart():
    """根据数据集信息，推荐chart
    Args
        postdata: {
            "instruction": <用户提示>,
            "dataset": {},  // 格式与【/ai-assistant/va】中保持一致
       }
    Return
    """
    json_dict = request.json or {}
    form_dict = request.form
    post_data = {**json_dict, **form_dict}
    try:
        instruction = post_data["instruction"]
        dataset = post_data["dataset"]
        n = post_data.get("n", 3)
        c2x = Chat2X(instruction=instruction, dataset=dataset, use_rag=use_rag, query_engine=query_engine)
        chart_list = c2x.to_chart_list(n=n)
        result = dict(chart_list=chart_list)
        response = dict(code=200, msg="操作成功", data=result, time=get_millisecond(), total=0)
    except Exception as e:
        response = dict(code=2000, msg=str(traceback.format_exc()), data={}, time=get_millisecond(), total=0)
    return response

@app.route("/ai-assistant/va/test", methods=["POST"])
def test_chart_config():
    """
    Args
        postdata: {
        "chart": "Radar",     // chart 名称
       }
    :return:
    """
    json_dict = request.json or {}
    form_dict = request.form
    post_data = {**json_dict, **form_dict}

    chart_name = post_data["chart"]

    try:
        mock = mock_dataset(chart_name)
        instruction = mock["instruction"]
        dataset = mock["dataset"]

        c2c = Chat2X(instruction=instruction, dataset=dataset)
        config = c2c.to_config()
        app.logger.info(f"\n------------------ Chart Config ------------------\n{json.dumps(config, ensure_ascii=False)}")
        result = dict(config=config, mock=mock)
        response = dict(code=200, msg="操作成功", data=result, time=get_millisecond(), total=0)
    except Exception as e:
        response = dict(code=2000, msg=str(e), data={}, time=get_millisecond(), total=0)
    return response

if __name__ == "__main__":
    # 是否开启 DEBUG 模式
    app.debug = True

    app.logger.addHandler(console_handler)
    logger = app.logger      # 获取 Flask 的默认 logger
    # 添加处理器到 logger
    logger.addHandler(console_handler if app.debug else file_handler)
    # 防止 Response 中的中文为 Unicode
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=8888)




