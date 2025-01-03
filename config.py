import os
from dotenv import load_dotenv

# 根据环境加载不同的 .env 文件
if os.environ.get("FLASK_ENV") == "production":
    load_dotenv(".env.production")  # 加载生产环境的配置
else:
    load_dotenv(".env")  # 加载测试环境的配置


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")

    BUSUANZI_JWT_SECRET_KEY = os.getenv("BUSUANZI_JWT_SECRET_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    # 阿里配置文件
    ALI_API_KEY = os.getenv("ALI_API_KEY")
    ALI_API_URL = os.getenv("ALI_API_URL")

    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 1))

    WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN")
    WECHAT_WEBHOOK_TOKEN = os.getenv("WECHAT_WEBHOOK_TOKEN")


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")


config_env = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
