import logging


class Logger:
    def __init__(self, log_file="app.log"):
        self.log_file = log_file
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename=self.log_file,  # 日志文件名
            level=logging.INFO,  # 设置日志级别
            format="%(asctime)s - %(levelname)s - %(message)s",  # 日志格式
            datefmt="%Y-%m-%d %H:%M:%S",  # 日期格式
        )

    def info(self, message):
        logging.info(message)

    def warning(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)

    def debug(self, message):
        logging.debug(message)
