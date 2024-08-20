import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://root:example@localhost:27017')

    REDIS_URL = 'redis://localhost:6379'
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL
    CACHE_DEFAULT_TIMEOUT = 600  # 10 минут
