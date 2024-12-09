import os
from dotenv import load_dotenv

# 根据环境加载不同的 .env 文件
if os.environ.get('FLASK_ENV') == 'production':
    load_dotenv('.env.production')  # 加载生产环境的配置
else:
    load_dotenv('.env')  # 加载测试环境的配置

class BaseConfig:
    SECRET_KEY = "your secret key"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    # 缓存配置
    CACHE_TYPE = os.getenv('CACHE_TYPE')
    CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST')
    CACHE_REDIS_PORT = os.getenv('CACHE_REDIS_PORT')

    # 阿里配置文件
    ALI_API_KEY = os.getenv('ALI_API_KEY')
    ALI_API_URL = os.getenv('ALI_API_URL')


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI =  os.getenv('SQLALCHEMY_DATABASE_URI')


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}