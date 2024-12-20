from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from redis import Redis
import os
from dotenv import load_dotenv

db = SQLAlchemy()
cache = Cache()

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_db = int(os.getenv("REDIS_DB", 2))


redis = Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)
