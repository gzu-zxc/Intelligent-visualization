from enum import Enum

class ChartType(Enum):
    VisualExplorer, Quick, Mark = range(3)

class VisualRole(Enum):
    Dimension = "dimension"
    Measure = "measure"

class VisualType(Enum):
    Nominal = "nominal"
    Quantitative = "quantitative"

class SemanticRole(Enum):
    Empty = ""
    Longitude = "[Geographical].[Longitude]"
    Latitude = "[Geographical].[Latitude]"
    Country = "[Country].[Name]"
    Province = "[State].[Name]"
    City = "[City].[Name]"
    County = "[County].[Name]"

class SplitTime(Enum):
    Year = "SPLIT_YEAR"
    Season = "SPLIT_SEASON"
    Month = "SPLIT_MONTH"
    Day = "SPLIT_DAY"
    Hour = "SPLIT_HOUR"
    Minute = "SPLIT_MINUTE"
    Season_4 = "SPLIT_SEASON_4" # 1-4
    Second = "SPLIT_SECOND"     # 1-12
    Month_12 = "SPLIT_MONTH_12"     # 1-12
    Week_53 = "SPLIT_WEEK_53"   # 1-53
    Weekday_7 = "SPLIT_WEEKDAY_7"   # 1-7
    Day_31 = "SPLIT_DAY_31"     # 1-31
    Hour_24 = "SPLIT_HOUR_24"       # 0-24
    Minute_60 = "SPLIT_MINUTE_60"   # 0-59
    Second_60 = "SPLIT_SECOND_60"   # 0-59

ALL_CHARTS = {
    # ------------------可视化探索器-----------------
    "bar": ("条形图", ChartType.Mark.value),
    "line": ("折线图", ChartType.Mark.value),
    "area": ("区域图", ChartType.Mark.value),
    "square": ("方向。目前只有显示为地图才支持此图形。", ChartType.Mark.value),
    "circle": ("圆", ChartType.Mark.value),
    "shape": ("形状", ChartType.Mark.value),
    "text": ("文本", ChartType.Mark.value),
    "pie": ("饼图", ChartType.Mark.value),
    "doughnut": ("环状饼图", ChartType.Mark.value),

    "BarStack": ("堆叠条", ChartType.VisualExplorer.value),
    "BarHoriz": ("柱状图", ChartType.VisualExplorer.value),
    "Circle": ("圆视图（散点图）", ChartType.VisualExplorer.value),
    "DimArea": ("面积图（离散）", ChartType.VisualExplorer.value),
    "DimLine": ("折线图（离散）", ChartType.VisualExplorer.value),
    "FilledMaps": ("填充地图", ChartType.VisualExplorer.value),
    "Maps": ("符号地图", ChartType.VisualExplorer.value),
    "IndicatorCard": ("指标卡", ChartType.VisualExplorer.value),
    "Pies": ("饼图", ChartType.VisualExplorer.value),
    "WordCloud": ("词云图", ChartType.VisualExplorer.value),
    # ------------------快速图表-----------------
    "Table": ("表格", ChartType.Quick.value),
    "Radar": ("雷达图", ChartType.Quick.value),
    "PivotTable": ("交叉表", ChartType.Quick.value),
    "Funnel": ("漏斗图", ChartType.Quick.value),
    "RectangularTree": ("矩形树图", ChartType.Quick.value),
}

MARK_ENOCIDNGS_TO_ROLE = {
    "text-encoding": (VisualRole.Dimension.value, VisualRole.Measure.value),
    "color-encoding": (VisualRole.Dimension.value),
    "size-encoding": (VisualRole.Measure.value),
    "wedge-size-encoding": (VisualRole.Measure.value),
    "shape-encoding": (VisualRole.Dimension.value),
    "tooltip-encoding": (),
    "level-of-detail-encoding-encoding": (),
}
ALL_MARK_ENCODINGS = {
        "bar": ["color-encoding"], # "text-encoding", "size-encoding", "level-of-detail-encoding", "tooltip-encoding",
        "line": ["color-encoding", "text-encoding", "size-encoding"], # "level-of-detail-encoding", "tooltip-encoding",
        "area": ["color-encoding", "text-encoding"], # "level-of-detail-encoding", "tooltip-encoding",
        "square": ["color-encoding", "text-encoding", "size-encoding"], # "level-of-detail-encoding", "tooltip-encoding",
        "circle": ["color-encoding", "text-encoding", "size-encoding"], # "level-of-detail-encoding", "tooltip-encoding",
        "shape": ["color-encoding", "text-encoding", "size-encoding"], # "level-of-detail-encoding", "tooltip-encoding", "shape-encoding"
        "text": [
            "text-encoding",
            "color-encoding",
            "size-encoding",
            # "level-of-detail-encoding",
            # "tooltip-encoding",
        ],
        "multipolygon": ["color-encoding"], # "text-encoding", "size-encoding", "level-of-detail-encoding", "tooltip-encoding"
        "pie": ["color-encoding", "text-encoding", "size-encoding", "wedge-size-encoding"], # "level-of-detail-encoding", "tooltip-encoding",
        "gantt": ["color-encoding", "text-encoding", "size-encoding"],  #"level-of-detail-encoding", "tooltip-encoding",
        "polygon": ["color-encoding"],  # "sort-encoding", "level-of-detail-encoding", "tooltip-encoding",
        "heatmap": ["color-encoding", "text-encoding", "size-encoding"],  #"level-of-detail-encoding", "tooltip-encoding",
        "doughnut": ["color-encoding", "text-encoding", "size-encoding"
            # "level-of-detail-encoding",
            # "tooltip-encoding",
            # {
            #     "encodingType": "wedge-size-encoding",
            #     "marksCardDropdownItem": {
            #         "dropdownEncodingType": "wedge-size-encoding",
            #         "encodingFieldVector": [],
            #         "radius": 1,
            #         "radius0": 0.5,
            #     },
            # },
        ]
    }


class ChartConfig(object):
    def __init__(self, dataset, chart_name, table, target, group_by, order_by, geo_role, date_split,
                 filter, refline):
        # 数据集信息
        self.dataset = dataset
        # LLM 响应内容
        self.chart_name = chart_name
        self.table = table
        self.target = target
        self.group_by = group_by
        self.order_by = order_by
        self.geo_role = geo_role
        self.date_split = date_split
        self.filter_list = filter
        self.refline_list = refline

    def get_mark_encodings(self, mark_type):
        return ALL_MARK_ENCODINGS[mark_type]

    def get_config_type(self):
        return ALL_CHARTS[self.chart_name]

    def infer_shelf(self):
        """Pie, WordCloud, IndicatorCard 单独配置 mark 可用
        """
        # 默认取值
        rows, cols = [], []
        mark = []
        if self.chart_name == "BarHoriz":
            # 柱状图，不用设置标记（mark），只需要配置行（rows）和列（columns）即可，所以其配置在行列字段架（shelf）中
            # 默认 rows 存储 mea(>=1)，columns 存储 dim(>=1)
            for alias in self.group_by:  # dim
                field = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                               visual_role=VisualRole.Dimension.value)
                cols.append(field)

            for item in self.target:  # mea
                alias = item["field"]
                agg = item["agg"]
                field = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                               visual_role=VisualRole.Measure.value)
                rows.append(field)
        elif self.chart_name == "BarStack":
            # 1 个日期
            # dim >=1, mea >=1
            for alias in self.group_by:  # dim
                if len(cols) == len(self.group_by) - 1: # group_by 中的最后一个元素用作 color 标记
                    break
                field = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                               visual_role=VisualRole.Dimension.value)
                cols.append(field)

            for item in self.target:  # mea
                alias = item["field"]
                agg = item["agg"]
                field = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                               visual_role=VisualRole.Measure.value)
                rows.append(field)
            mark = self.infer_mark(mark_type="bar")
        elif self.chart_name == "Circle":
            # dim >=1, mea >=1
            for alias in self.group_by:  # dim
                field = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                               visual_role=VisualRole.Dimension.value)
                cols.append(field)

            for item in self.target:  # mea
                alias = item["field"]
                agg = item["agg"]
                field = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                               visual_role=VisualRole.Measure.value)
                rows.append(field)
            mark = self.infer_mark(mark_type="circle")
        elif self.chart_name == "DimLine":
            # TODO 判断是否需要 mark
            # TODO 判断 dateSplit
            # dim >=0, mea >=1
            for alias in self.group_by:  # dim
                field = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                               visual_role=VisualRole.Dimension.value)
                cols.append(field)

            for item in self.target:  # mea
                alias = item["field"]
                agg = item["agg"]
                field = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                               visual_role=VisualRole.Measure.value)
                rows.append(field)
            mark = self.infer_mark(mark_type="line")
        elif self.chart_name == "DimArea":
            # TODO 判断是否需要 mark
            # TODO 判断 dateSplit
            # dim >=0, mea >=1
            for alias in self.group_by:  # dim
                field = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                               visual_role=VisualRole.Dimension.value)
                cols.append(field)

            for item in self.target:  # mea
                alias = item["field"]
                agg = item["agg"]
                field = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                               visual_role=VisualRole.Measure.value)
                rows.append(field)
            mark = self.infer_mark(mark_type="area")
        elif self.chart_name == "WordCloud":
            # dim >1
            # mea >1
            # 行列不能指定字段，需配置一个大小标记，颜色、文本、详细信息至少指定其中一个标记
            mark = self.infer_mark(mark_type="text")
        elif self.chart_name == "Pies":
            if len(self.group_by) > 1:
                for alias in self.group_by[:-1]:  # dim
                    field = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                                   visual_role=VisualRole.Dimension.value)
                    cols.append(field)
            mark = self.infer_mark(mark_type="pie")
        elif self.chart_name == "FilledMaps":
            # 地理维度=1, 1 经度, 1 纬度。通过修改字段的地理角色，将字段设置为经度或者纬度
            # 列有且只有一个字段为经度，行有且只有一个字段为纬度
            # mark中，还需指定一个字段地理角色，是非经纬度角色，如省/自治区
            # dim >=0, mea >=1
            latitude_field = self.infer_base_config(table="", alias="Latitude (generated)", agg="COUNT",
                                                    visual_role=VisualRole.Dimension.value,
                                                    semantic_role=SemanticRole.Latitude.value)
            rows.append(latitude_field)

            longitude_field = self.infer_base_config(table="", alias="Longitude (generated)", agg="COUNT",
                                                     visual_role=VisualRole.Dimension.value,
                                                     semantic_role=SemanticRole.Longitude.value)
            cols.append(longitude_field)
            mark = self.infer_mark("multipolygon")
        elif self.chart_name == "Maps":
            # 地理维度=1, 1 经度, 1 纬度。通过修改字段的地理角色，将字段设置为经度或者纬度
            # 列有且只有一个字段为经度，行有且只有一个字段为纬度
            # mea: [0-2]
            latitude_field = self.infer_base_config(table="", alias="Latitude (generated)", agg="COUNT",
                                           visual_role=VisualRole.Dimension.value, semantic_role=SemanticRole.Latitude.value)
            rows.append(latitude_field)

            longitude_field = self.infer_base_config(table="", alias="Longitude (generated)", agg="COUNT",
                                           visual_role=VisualRole.Dimension.value, semantic_role=SemanticRole.Longitude.value)
            cols.append(longitude_field)
            mark = self.infer_mark("circle")
        elif self.chart_name == "IndicatorCard":
            # mea >= 1
            mark = self.infer_mark(mark_type="text")
        else:
            raise Exception(f"Chart 类型：{self.chart_name} 暂未实现！")

        shelf = dict(rows=rows, columns=cols)
        return shelf, mark

    def _infer_mark_pie(self, enc_type, visual_role):
        """ pie 标记类型
        - 可单独配置
        - 可结合 shelf 配置
        """
        if visual_role == VisualRole.Dimension.value:
            # dim
            alias = self.group_by[-1]
            base_config = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                                 visual_role=visual_role)
        elif visual_role == VisualRole.Measure.value:
            # mea
            alias = self.target[0]["field"]
            agg = self.target[0]["agg"]
            base_config = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                                 visual_role=visual_role)
        else:
            base_config = None
        enc_obj = {
            "isVisible": True,
            "isEnabled": False if enc_type == "wedge-size-encoding" else True,
            "encodingType": enc_type,
            "encodingFieldVector": [base_config] if base_config else []
        }
        return enc_obj

    def _infer_mark_text(self, enc_type, visual_role):
        enc_vec_list = []
        if visual_role == VisualRole.Dimension.value:
            # 维度：groupby中的属性
            if len(self.group_by) > 0:
                alias = self.group_by[0]
                base_config = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                                     visual_role=visual_role)
                enc_vec_list.append(base_config)
            else:
                enc_vec_list = []
        elif visual_role == VisualRole.Measure.value or len(visual_role) == 2:
            # 度量
            for item in self.target:
                alias = item["field"]
                agg = item["agg"]
                base_config = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                                     visual_role=visual_role)
                enc_vec_list.append(base_config)
        else:
            enc_vec_list = []
        enc_obj = {
            "isVisible": True,
            "isEnabled": False if enc_type == "wedge-size-encoding" else True,
            "encodingType": enc_type,
            "encodingFieldVector": enc_vec_list
        }
        return enc_obj

    def _infer_mark_bar(self, enc_type, visual_role):
        if visual_role == VisualRole.Dimension.value:
            # 维度：groupby中的属性, TODO 需要优化这里的判断
            if len(self.group_by) > 0:
                alias = self.group_by[-1] if len(self.group_by) > 1 else self.group_by[0]
                base_config = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                                     visual_role=visual_role)
            else:
                base_config = None
        elif visual_role == VisualRole.Measure.value:
            # 度量
            alias = self.target[0]["field"]
            agg = self.target[0]["agg"]
            base_config = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                                 visual_role=visual_role)
        else:
            base_config = None
        enc_obj = {
            "isVisible": True,
            "isEnabled": False if enc_type == "wedge-size-encoding" else True,
            "encodingType": enc_type,
            "encodingFieldVector": [base_config] if base_config else []
        }
        return enc_obj

    def _infer_mark_line(self, enc_type, visual_role):
        return self._infer_mark_bar(enc_type, visual_role)

    def _infer_mark_area(self, enc_type, visual_role):
        return self._infer_mark_bar(enc_type, visual_role)
    def _infer_mark_square(self, enc_type, visual_role):
        if visual_role == VisualRole.Dimension.value:
            # 维度：groupby中的属性, TODO 需要优化这里的判断
            alias = self.group_by[0]
            base_config = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                                 visual_role=visual_role)
        elif visual_role == VisualRole.Measure.value:
            # 度量
            alias = self.target[0]["field"]
            agg = self.target[0]["agg"]
            base_config = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                                 visual_role=visual_role)
        else:
            base_config = None
        enc_obj = {
            "isVisible": True,
            "isEnabled": False if enc_type == "wedge-size-encoding" else True,
            "encodingType": enc_type,
            "encodingFieldVector": [base_config] if base_config else []
        }
        return enc_obj

    def _infer_mark_circle(self, enc_type, visual_role):
        if len(self.group_by) == 0:
            raise Exception("未识别出维度信息，请换个问题试试")
        if len(self.target) == 0:
            raise Exception("未识别出度量信息，请换个问题试试")

        if visual_role == VisualRole.Dimension.value:
            # 维度
            alias = self.group_by[0]
            base_config = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                                 visual_role=visual_role, semantic_role=self.geo_role)
        elif visual_role == VisualRole.Measure.value:
            # 度量
            alias = self.target[0]["field"]
            agg = self.target[0]["agg"]
            base_config = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                                 visual_role=visual_role)
        else:
            base_config = None
        enc_obj = {
            "isVisible": True,
            "isEnabled": False if enc_type == "wedge-size-encoding" else True,
            "encodingType": enc_type,
            "encodingFieldVector": [base_config] if base_config else []
        }
        return enc_obj

    def _infer_mark_shape(self, enc_type, visual_role):
        if visual_role == VisualRole.Dimension.value:
            # 维度：groupby中的属性, TODO 需要优化这里的判断
            alias = self.group_by[-1] if len(self.group_by[0]) > 1 else self.group_by[0]
            base_config = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                                 visual_role=visual_role)
        elif visual_role == VisualRole.Measure.value:
            # 度量
            alias = self.target[0]["field"]
            agg = self.target[0]["agg"]
            base_config = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                                 visual_role=visual_role)
        else:
            base_config = None
        enc_obj = {
            "isVisible": True,
            "isEnabled": False if enc_type == "wedge-size-encoding" else True,
            "encodingType": enc_type,
            "encodingFieldVector": [base_config] if base_config else []
        }
        return enc_obj
    def _infer_mark_doughnut(self, enc_type, visual_role):
        return self._infer_mark_shape(enc_type, visual_role)

    def _infer_mark_multipolygon(self, enc_type, visual_role):
        if visual_role == VisualRole.Dimension.value:
            # 维度
            alias = self.group_by[0]
            base_config = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                                 visual_role=visual_role, semantic_role=self.geo_role)
        else:
            base_config = None
        enc_obj = {
            "isVisible": True,
            "isEnabled": False if enc_type == "wedge-size-encoding" else True,
            "encodingType": enc_type,
            "encodingFieldVector": [base_config] if base_config else []
        }
        return enc_obj

    def infer_mark(self, mark_type=None):
        if mark_type is None:
            mark_type = self.chart_name
        # 默认取值
        # TODO 需要根据 chart 类型进行推断
        mark = []

        mark_obj = dict(markType=mark_type, encodings=[])
        encodings = self.get_mark_encodings(mark_type=mark_type)
        for enc_type in encodings:
            if enc_type in MARK_ENOCIDNGS_TO_ROLE and len(MARK_ENOCIDNGS_TO_ROLE[enc_type])>0:
                visual_role = MARK_ENOCIDNGS_TO_ROLE[enc_type]
            else:
                visual_role = None
            #############  Pie, WordCloud, IndicatorCard 单独配置 mark 可用 #############
            if mark_type == "pie":
                enc_obj = self._infer_mark_pie(enc_type, visual_role)
            #############  以下 mark 需要搭配 shelf 可用 #############
            elif mark_type == "text":
                # dim >=1 | mea >=1
                enc_obj = self._infer_mark_text(enc_type, visual_role)
            elif mark_type == "bar":
                # dim >=1 | mea >=1
                enc_obj = self._infer_mark_bar(enc_type, visual_role)
            elif mark_type == "line":
                # 1 个日期
                # dim >=0 | mea >=1
                enc_obj = self._infer_mark_line(enc_type, visual_role)
            elif mark_type == "area":     # 与 line 逻辑相同
                # 1 个日期
                # dim >=0 | mea >=1
                enc_obj = self._infer_mark_area(enc_type, visual_role)
            elif mark_type == "square":
                # 只有地图才支持此图形
                # 1 个地理维度，包含 1 经度 1 纬度
                # 对于符号地图， 有且仅有一个字段为经度，行有且只有一个字段为维度
                # 0-2 度量
                # TODO 配置 size-encoding 时，没有target？
                enc_obj = self._infer_mark_square(enc_type, visual_role)
            elif mark_type == "circle":
                enc_obj = self._infer_mark_circle(enc_type, visual_role)
            elif mark_type == "shape":
                # TODO 配置 size-encoding 时，没有target？
                enc_obj = self._infer_mark_shape(enc_type, visual_role)
            elif mark_type == "doughnut":
                # TODO 配置 size-encoding 时，没有target？
                enc_obj = self._infer_mark_doughnut(enc_type, visual_role)
            elif mark_type == "multipolygon":
                # dim >=1 | mea >=1
                enc_obj = self._infer_mark_multipolygon(enc_type, visual_role)
            else:
                raise Exception(f"可视化探索器不存在图形：{self.chart_name}！")
            if enc_obj:
                mark_obj["encodings"].append(enc_obj)
        mark.append(mark_obj)
        return mark

    def infer_chart_config(self):
        """
        前置约束：templateType == "Quick"

        Args
            chart_name: Table | Radar | PivotTable | Funnel | RectangularTree
        """
        # 默认取值
        chart_config = {}
        if self.chart_name == "Table":
            # table 按 dim, mea 顺序展示所有内容
            field_list = []
            for alias in self.group_by: # dim
                field = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                               visual_role=VisualRole.Dimension.value)
                field_list.append(field)

            for item in self.target:   # mea
                alias = item["field"]
                agg = item["agg"]
                field = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                               visual_role=VisualRole.Measure.value)
                field_list.append(field)
            visual_option = {
                "values": {
                    "name": "数据",
                    "fields": field_list,
                }
            }
        elif self.chart_name == "Radar":
            # - dim: 1, mea: >=1
            # - dim: 2, mea: 1
            x_field_list, y_field_list = [], []
            alias = self.group_by[0]    # dim, 最大长度 1
            x_field = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                           visual_role=VisualRole.Dimension.value)
            x_field_list.append(x_field)

            alias = self.target[0]["field"]  # mea, 最大长度 1
            agg = self.target[0]["agg"]
            y_field = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                           visual_role=VisualRole.Measure.value)
            y_field_list.append(y_field)
            visual_option = {
                "x": {
                    "name": "x轴",
                    "fields": x_field_list,  # 支持一个 dim 字段
                    "max": 1,
                },
                "y": {
                    "name": "y轴",
                    "fields": y_field_list,  # 支持一个 measure 字段
                    "max": 1,
                },
                # TODO series @吴凯凯
                "series": {
                    "name": "分组",
                    "fields": [],
                    "max": 1,
                    "min": 0,
                }
            }
        elif self.chart_name == "PivotTable":
            # rows, columns 为 dim, 默认都写在 row 里面 TODO 以后可酌情优化
            # values 为 mea
            rows, cols, vals = [], [], []
            for alias in self.group_by:  # dim
                field = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                               visual_role=VisualRole.Dimension.value)
                rows.append(field)

            for item in self.target:  # mea
                alias = item["field"]
                agg = item["agg"]
                field = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                               visual_role=VisualRole.Measure.value)
                vals.append(field)
            visual_option = {
                "rows": {
                    "name": "行",
                    "fields": rows,
                },
                "columns": {
                    "name": "列",
                    "fields": cols,
                },
                "values": {
                    "name": "值",
                    "fields": vals,
                },
            }
        elif self.chart_name == "Funnel":
            cats, vals = [], []
            alias = self.group_by[0]  # dim, 最大长度 1
            cat_field = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                             visual_role=VisualRole.Dimension.value)
            cats.append(cat_field)

            for item in self.target:  # mea
                alias = item["field"]
                agg = item["agg"]
                field = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                               visual_role=VisualRole.Measure.value)
                vals.append(field)
            visual_option = {
                "categories": {
                    "name": "分类（维度）",
                    "fields": cats,
                    "role": [VisualRole.Dimension.value],
                    "min": 1,
                    "max": 1,
                },
                "values": {
                    "name": "数据（度量）",
                    "fields": vals,
                    "role": [VisualRole.Measure.value],
                    "min": 1,
                },
            }
        elif self.chart_name == "RectangularTree":
            cats, vals = [], []
            for alias in self.group_by:  # dim
                field = self.infer_base_config(table=self.table, alias=alias, agg="COUNT",
                                               visual_role=VisualRole.Dimension.value)
                cats.append(field)
                if len(cats) == 2:
                    break

            # mea
            alias = self.target[0]["field"]
            agg = self.target[0]["agg"]
            field = self.infer_base_config(table=self.table, alias=alias, agg=agg,
                                           visual_role=VisualRole.Measure.value)
            vals.append(field)

            visual_option = {
                "categories": {
                    "name": "分类（维度）",
                    "fields": cats,
                    "role": [VisualRole.Dimension.value],
                    "min": 1,
                    "max": 2,
                },
                "values": {
                    "name": "数据（度量）",
                    "fields": vals,
                    "role": [VisualRole.Measure.value],
                    "min": 1,
                    "max": 1,
                },
            }
        else:
            raise Exception(f"快速图表： {self.chart_name} 不存在")
        chart_config[self.chart_name] = visual_option
        return chart_config

    def infer_base_config(self, table, alias, agg, visual_role, semantic_role=None, date_split=""):
        """
        需要推断的内容：
        alias: 属性别名（中文名称）
        aggregation: SUM | COUNT | ...
        groupBy: "groupby" | null,
        orderBy: "orderby" | null,
        filter: "??" | null,
        visualRole: dimension | measure
        visualType: quantitative | nominal
        visualDatatype: "real" | "string" | ...
        """
        if table:
            field = self.dataset.get_field(table=table, alias=alias)
            hash = self.dataset.get_hash(table=table, alias=alias)
            dtype = self.dataset.get_dtype(table=table, alias=alias)
        else:   # 为 ""
            assert "Latitude" in alias or "Longitude" in alias
            field = {"type": "dim", "subType": None, "operation": "null"}
            hash = ""
            dtype = "number"

        return {
        "alias": alias,
        "type": field["type"],
        "subType": field["subType"],
        "operation": field["operation"],
        "hash": hash,
        "aggregation": agg,
        "dateSplit": date_split,
        # "dataTable": "",
        "filter": None,
        "orderBy": self.order_by,
        "groupBy": agg or "group_by",
        # "calculationBasis": "",
        "visualRole": visual_role,
        "visualDatatype": dtype,
        "visualType": VisualType.Quantitative.value if visual_role == VisualRole.Measure.value
                                                        else VisualType.Nominal.value,
        "semanticRole": semantic_role
    }

    def infer_filters(self):
        """TEXT, Category, Date, String"""
        filters = []
        for item in self.filter_list:
            if not item["field"]:
                continue
            type = item["type"]
            alias = item["field"]
            field_obj = self.dataset.get_field(table=self.table, alias=alias)
            filter = {"field": field_obj}
            if type == FilterType.ListSelection.value:
                filter["normal"] = dict(type=type, data=[], chooseData=item["value_list"], customData=[], exclude=False)
            elif type == FilterType.UseAll.value:
                filter["normal"] = dict(type=type, data=[], chooseData=[], customData=[], exclude=False)
            elif type == FilterType.StringMatch.value:
                filter["wildcard"] = dict(type=item["method"], matchValue="", exclude=False)
            elif type == FilterType.ValueRange.value:
                filter["number"] = dict(type=type, min=item["min"], max=item["max"])
            elif type == FilterType.SpecialValue.value:
                filter["number"] = dict(type=type, specialValue=item["value"])
            elif FilterType.DateRange.value:
                filter["date"] = dict(type=type, min=item["min"], max=item["max"])
            elif FilterType.RelativeDate.value:
                filter["date"] = dict(type=type, relativeDate={"type": item["date_type"], "relative": item["relative"],
                                                               "before": item["before"], "after": item["after"]})
            else:
                raise Exception(f"Filter Type 不存在：{type}")
            filters.append(filter)
        return filters

    def infer_reflines(self):
        """支持 4 类参考线：
        refline: 参考线
        refband: 区间
        distband: 分布
        boxplot: 盒须图
        """
        reflines = []
        for item in self.refline_list:
            if not item["type"]:
                continue
            type = item["type"]
            field_obj = self.dataset.get_field(table=self.table, alias=self.target)
            if type == "constant":
                refline = dict(formula=type, axisColumn=field_obj, value=item["value"])
            else:
                refline = dict(formula=type, axisColumn=field_obj)
            reflines.append(refline)
        return reflines


    def dump(self):
        """返回完整的 chart 配置"""
        visual_config = dict(templateType="", template="", shelf={}, mark=[], chart_config={},
                             filters=[], referenceLines=[])

        # ------------ templateType & template ------------#
        _, cfg_type = self.get_config_type()
        if cfg_type == ChartType.Mark.value:
            visual_config["templateType"] = "VisualExplorer"
            visual_config["template"] = "VisualExplorer"
            # ------------ mark ------------#
            visual_config["mark"] = self.infer_mark()
        elif cfg_type == ChartType.Quick.value:
            visual_config["templateType"] = "Quick"
            visual_config["template"] = self.chart_name
            # ------------ chart_config ------------#
            visual_config["chart_config"] = self.infer_chart_config()
        else:  # Shelf
            visual_config["templateType"] = "VisualExplorer"
            visual_config["template"] = self.chart_name
            # ------------ shelf ------------#
            visual_config["shelf"], visual_config["mark"] = self.infer_shelf()

        # 过滤操作
        visual_config["filters"] = self.infer_filters()

        # 参考线
        visual_config["reflines"] = self.infer_reflines()
        return dict(visual_config=visual_config)


class FilterType(Enum):
    #-------- 常规--------
    ListSelection = "listSelection"
    UseAll = "useAll"   # 不过滤
    # -------- 数值型 --------
    ValueRange = "valueRange"
    SpecialValue = "specialValue"
    # -------- 通配符型 --------
    StringMatch = "string_match"
    # -------- 日期型 --------
    DateRange = "dateRange"
    RelativeDate = "relativeDate"
