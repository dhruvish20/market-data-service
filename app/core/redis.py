import os
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
REDIS_TTL = int(os.getenv("REDIS_TTL", 300))  

redis_client = redis.Redis(host = REDIS_HOST, port = REDIS_PORT, db = REDIS_DB, decode_responses = True)

def get_redis_client():
    return redis_client

def set_cache(key: str, value: str, ttl: int = REDIS_TTL):
    redis_client.set(key, value, ex=ttl)

def get_cache(key: str):
    return redis_client.get(key)

