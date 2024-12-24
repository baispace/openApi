from flask import Flask, current_app
from exts import db, cache, redis
from blueprints.ai import bp as ai_bp
from blueprints.busuanzi import bp as busuanzi_bp
from blueprints.front import bp as front_bp
from flask_cors import CORS
from config import config_env
import os

app = Flask(__name__)

# 根据环境加载不同的 .env 文件
config_name = os.environ.get("FLASK_ENV", "development")
app.config.from_object(config_env.get(config_name))

db.init_app(app)
cache.init_app(app)
CORS(app)
redis.__init__(
    host=app.config["REDIS_HOST"],
    port=app.config["REDIS_PORT"],
    db=app.config["REDIS_DB"],
    decode_responses=True,
)

# 注册蓝图
app.register_blueprint(ai_bp)
app.register_blueprint(busuanzi_bp)
app.register_blueprint(front_bp)

if __name__ == "__main__":
    app.run()
