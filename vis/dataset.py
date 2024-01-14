from enum import Enum

class ChartType(Enum):
    VisualExplorer, Quick, Mark = range(3)

class VisualType(Enum):
    Nominal = "nominal"
    Quantitative = "quantitative"


class Dataset(object):
    def __init__(self, dataset):
        """
        Args
            dataset: 数据集元信息，是否涉及调用 Uniplore 服务接口获取信息？
            {
                "field": [
                    {
                         "dataTable": "student_score",
                         "fieldList": [{
                                "attribute": "name",
                                "alias": "姓名"
                                "type": "dim",
                                "subType": null,
                                "operation": "a8az8nx5xr3p6j7a75zrynab",
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
                "userDefinedField": [   // 可选参数
                {..}
                ]}
        """
        self.dataset = dataset

    def get_hash(self, table, alias):
        """获取属性的唯一标识"""
        hash = []
        custom_field_list = self.dataset["userDefinedField"] or [] if "userDefinedField" in self.dataset else []
        for item in self.dataset["field"]:
            if table == item["dataTable"]:
                hash = [attr["operation"] for attr in item["fieldList"] + custom_field_list if attr["alias"]==alias]
                break
        if len(hash) == 0:
            raise Exception(f"table: {table}, Alias: {alias} 不存在！")
        return hash[0]

    def get_dtype(self, table, alias):
        """获取属性类型"""
        dtype = []
        custom_field_list = self.dataset["userDefinedField"] or [] if "userDefinedField" in self.dataset else []
        for item in self.dataset["field"]:
            if table == item["dataTable"]:
                dtype = [attr["dataType"] for attr in item["fieldList"] + custom_field_list if attr["alias"]==alias]
                break
        if len(dtype) == 0:
            raise Exception(f"table: {table}, Alias: {alias} 不存在！")
        return dtype[0]

    def get_field(self, table, alias):
        field = []
        custom_field_list = self.dataset["userDefinedField"] or [] if "userDefinedField" in self.dataset else []
        for item in self.dataset["field"]:
            if table == item["dataTable"]:
                field = [attr for attr in item["fieldList"] + custom_field_list if attr["alias"] == alias]
                break
        if len(field) == 0:
            raise Exception(f"table: {table}, Alias: {alias} 不存在！")
        return field[0]

    def __str__(self):
        """作为 prompt 中的上下文信息

        ## 数据集
        表：sale (发货日期,行ID,订单ID,订单日期,快递方式,客户ID,客户名称,细分,城市,省自治区,国家,地区,产品ID,类别,子类别,产品名称,销售额,数量,折扣,利润)
        """
        dataset_info = "## 数据集\n"
        custom_field_list = self.dataset["userDefinedField"] or [] if "userDefinedField" in self.dataset else []
        for table in self.dataset["field"]:
            table_name = table["dataTable"]
            col_str = ", ".join([attr["alias"] for attr in table["fieldList"] + custom_field_list])
            dataset_info += f"表： {table_name} ({col_str})\n"
        dataset_info += "\n"
        return dataset_info







