from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from utils.Logger import Logger

db = SQLAlchemy()
redis = Redis()
logger = Logger()
