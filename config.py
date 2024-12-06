class BaseConfig:
    SECRET_KEY = "your secret key"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://api-dev:FZxaDGsN5f7DJSMw@39.106.227.149:3306/api-dev?charset = utf8mb4"

    # 缓存配置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379

    ALI_API_KEY = 'sk-ef91cf1db4b04a6b9851bbb87fda42e7'
    #ALI_API_URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
    ALI_API_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'

class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://[测试服务器MySQL用户名]:[测试服务器MySQL密码]@[测试服务器MySQL域名]:[测试服务器MySQL端口号] / pythonbbs?charset = utf8mb4"


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://api-dev:FZxaDGsN5f7DJSMw@39.106.227.149:3306/api-dev?charset = utf8mb4"

    # 缓存配置
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "127.0.0.1"
    CACHE_REDIS_PORT = 6379

    ALI_API_KEY = 'sk-ef91cf1db4b04a6b9851bbb87fda42e7'
    # ALI_API_URL = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation'
    ALI_API_URL = 'https://dashscope.aliyuncs.com/compatible-mode/v1'