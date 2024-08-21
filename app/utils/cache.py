import redis
import json

class Cache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.r = redis.Redis(host=host, port=port, db=db)

    def get(self, key: str):
        cached = self.r.get(key)
        if cached:
            return json.loads(cached)
        return None

    def set(self, key: str, value, ttl=3600):
        self.r.setex(key, ttl, json.dumps(value))
