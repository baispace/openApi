from flask import Flask
import config
from exts import db, cache

from blueprints.ai import bp as ai_bp
from blueprints.busuanzi import bp as busuanzi_bp
from blueprints.front import bp as front_bp


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config.from_object(config.DevelopmentConfig)

db.init_app(app)
cache.init_app(app)

# 注册蓝图
app.register_blueprint(ai_bp)
app.register_blueprint(busuanzi_bp)
app.register_blueprint(front_bp)

if __name__ == '__main__':
    app.run(debug=True)
