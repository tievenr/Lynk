import redis 
import random 
import string
import os

try:
    r = redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=6379,
        decode_responses=True,
        socket_connect_timeout=5
    )
    r.ping()
except redis.ConnectionError:
    print("WARNING: Redis not available")
    r = None

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def set_url(code: str, url: str):
    if r:
        r.set(code, url)

def get_url(code: str):
    if r:
        return r.get(code)
    return None