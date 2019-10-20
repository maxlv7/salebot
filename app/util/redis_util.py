import redis

from config import redis_config

pool = redis.BlockingConnectionPool(**redis_config, decode_responses=True)
redis_ = redis.Redis(connection_pool=pool)
