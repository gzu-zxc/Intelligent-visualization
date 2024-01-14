import json
import logging

from vis.chart_config import ChartConfig
from vis.prompt import prompt_template, subtask, context_info, gen_recommend_q_prompt, gen_recommend_chart_prompt,\
    sample_info, rag_prompt_template, intention_analysis_prompt_template, rag_intention_analysis_prompt_template
from vis.dataset import Dataset
from model_backend import ModelFactory, ModelType
from vis.chart_config import ALL_CHARTS, ChartType

# 获取与 Flask 应用相同的日志对象
logger = logging.getLogger('werkzeug')

class Chat2X(object):
    def __init__(self, instruction, dataset, use_rag=False, query_engine=None, history=[]):
        self.instruction = instruction
        self.dataset = Dataset(dataset)
        self.chart_config = None
        self.use_rag = use_rag
        self.query_engine = query_engine
        self.history = history

    def chat_with_gpt(self, prompt):
        # 用于与LLM进行交互的核心方法。它的主要作用是向聊天模型发送请求并获取响应。
        # 模型配置(ChatGPT)
        model_config = dict(temperature=0.2, top_p=1.0, n=1, stream=False,
                            max_tokens=None, presence_penalty=0.0, frequency_penalty=0.0)
        # llm_backend = ModelFactory.create(ModelType.GPT_3_5_TURBO, model_config)
        # llm_backend = ModelFactory.create(ModelType.TIGERBOT_13, model_config)
        llm_backend = ModelFactory.create(ModelType.Qwen_72, model_config)

        # 设置消息格式(ChatGPT)
        # 如果 self.history 存在，即之前有对话历史，那么这些历史消息会被加入到当前的消息列表中。每个消息都有一个角色（role），可以是 user 或其他，以及相应的内容（content）。
        # 如果没有历史消息，则仅创建一个包含用户当前输入的消息。
        if self.history:
            messages = [{"role": item["role"], "content": item["content"]} for item in self.history] + \
                        [{"role": "user", "content": prompt}]
        else:
            messages = [{"role": "user", "content": prompt}]

        # 获取响应结果(ChartGPT)
        response = llm_backend.run(messages=messages)
        result = response["choices"][0]["message"]["content"]
        return result

    def extract_json(self, string):
        """从 string 中提取 JSON 字符串,将其转换为 JSON 对象返回"""
        start = string.index("{")
        end = 0
        count = 1
        for end, c in enumerate(string[start + 1:], start=start + 1):
            if c == '}':
                count -= 1
            elif c == '{':
                count += 1
            if count == 0:
                break
        assert (count == 0)  # 检查是否找到最后一个'}'

        try:
            result = json.loads(string[start: end+1])
        except Exception as e:
            raise Exception(f"JSON 解析失败：{str(e)}")
        return result

    def intention_analysis(self):
        """分析用户意图
        - unreadable: 用户输入了不可读的内容
        - meaningless: 用户输入了与当前数据可视化场景无关的无意义的内容
        - identify_analysis_target: 基于系统中的数据信息，帮助用户识别出有意义、有价值的分析目标
        - gen_chart: 生成图表
        - recommend_q: 针对系统中的数据信息，向用户推荐 3-5 个问题，帮助用户进行有意义、有价值的可视化探索
        - gen_dashboard: 生成仪表盘
        - gen_hue: 生成配色
        Return:
            {"intention": "unreadable|....|gen_hue", "response": ""}
        """
        dataset_info = str(self.dataset)
        if self.use_rag:
            prompt = rag_intention_analysis_prompt_template.format(dataset_info=dataset_info, instruction=self.instruction)
            resp = self.query_engine.query(prompt).response
        else:
            prompt = intention_analysis_prompt_template.format(dataset_info=dataset_info, instruction=self.instruction)
            resp = self.chat_with_gpt(prompt)

        logger.info(f"\n----------- Intention Prompt ------------------\n{prompt}")
        logger.info(f"\n------------ LLM Response -----------\n{resp}")
        json_resp = self.extract_json(resp)
        logger.info(f"\n------------ JSON Response -----------\n{json_resp}")
        return json_resp

    def to_config(self):
        dataset_info = str(self.dataset)
        # 根据 self.use_rag 的值，选择不同的提示模板。如果启用了 RAG，使用 rag_prompt_template；否则，使用 prompt_template。
        if self.use_rag:
            prompt = rag_prompt_template.format(dataset_info=dataset_info, sample_info=sample_info,
                                                instruction=self.instruction)
            resp = self.query_engine.query(prompt).response
        else:
            prompt = prompt_template.format(subtask=subtask, dataset_info=dataset_info, sample_info=sample_info,
                                            context_info=context_info, instruction=self.instruction)
            resp = self.chat_with_gpt(prompt)

        logger.info(f"\n----------- Prompt ------------------\n{prompt}")
        json_resp = self.extract_json(resp)
        logger.info(f"\n------------ LLM Response -----------\n{json_resp}")

        # 解析结果
        table = json_resp["table"]
        chart = json_resp["chart"]
        target = json_resp["target"]
        order_by = json_resp["order_by"]
        group_by = json_resp["group_by"]
        geo_role = json_resp["geo_role"]
        date_split = json_resp["date_split"]
        filter = json_resp["filter"]
        refline = json_resp["refline"]

        # 修正 chart 是饼图（Pies | pie）时可能存在的问题
        if chart.lower() in ["pies", "pie"]:
            chart = "Pies"

        self.chart_config = ChartConfig(dataset=self.dataset, chart_name=chart, table=table, target=target,
                                        group_by=group_by, order_by=order_by, geo_role=geo_role, date_split=date_split,
                                        filter=filter, refline=refline)
        chart_config = self.chart_config.dump()
        return chart_config

    def to_q_list(self, n):
        """根据数据集信息，生成用户问题列表"""
        # self.dataset.
        prompt = gen_recommend_q_prompt.format(n=n, dataset=str(self.dataset))
        resp = self.chat_with_gpt(prompt)
        # 向LLM询问
        json_resp = self.extract_json(resp)
        logger.info(f"\n------------ LLM Response ----------------\n{json_resp}")
        q_list = json_resp["q_list"]
        return q_list

    def to_chart_list(self, n=3):
        """根据数据集信息，生成 chart 列表"""
        # to_chart_list 方法在 Chat2X 类中用于根据数据集信息生成推荐的图表（chart）列表。
        # self.dataset.
        chart_name_list = []
        for k, (v, typ) in ALL_CHARTS.items():
            # Bar(条形)
            if typ == ChartType.Mark.value and typ != "pie":
                continue
            chart_name_list.append("{}：{}".format(k, v))

        prompt = gen_recommend_chart_prompt.format(instruction=self.instruction, dataset=str(self.dataset),
                                                   chart_list=",".join(chart_name_list), n=n)
        resp = self.chat_with_gpt(prompt)
        json_resp = self.extract_json(resp)
        logger.info(f"\n------------ LLM Response ----------------\n{json_resp}")
        chart_list = json_resp["chart_list"]
        return chart_list











