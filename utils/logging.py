import logging


# 配置日志
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')

# 创建一个处理器，用于输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # 控制台输出 DEBUG 及以上级别的日志
console_handler.setFormatter(log_formatter)

# 创建一个处理器，用于输出到文件
file_handler = logging.FileHandler('log/app.log')
file_handler.setLevel(logging.INFO)  # 文件输出 INFO 及以上级别的日志
file_handler.setFormatter(log_formatter)
