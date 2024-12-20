from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from redis import Redis

db = SQLAlchemy()
cache = Cache()
redis = Redis()
