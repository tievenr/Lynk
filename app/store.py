import redis 
import random 
import string 

r = redis.Redis(host="redis", port=6379, decode_responses=True)

def generate_code(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def set_url(code: str, url: str):
    r.set(code, url)

def get_url(code: str):
    return r.get(code)