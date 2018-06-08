# utils/zlcache.py

import memcache

cache = memcache.Client(['139.199.131.146:11211'],debug=True)

def set(key,value,timeout=60):     #过期时间60s
    return cache.set(key,value,timeout)

def get(key):
    return cache.get(key)

def delete(key):
    return cache.delete(key)

