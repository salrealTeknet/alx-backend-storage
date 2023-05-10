#!/usr/bin/env python3
""" Writing string to Redis"""
from typing import Union, Callable, Optional, Any
import redis
import uuid
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ takes in input and output for a particular function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def count_calls(method: Callable) -> Callable:
    """takes into account the number of times Cache class are called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ wrapped function """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


class Cache:
    """ cache class defined """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ generate a random key (e.g. using uuid), store the input data in
        Redis using the random key and return the key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ take a key string argument and an optional Callable argument named
            fn. This callable will be used to convert the data back to the
            desired format """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ automatically parametrize Cache.get to str """
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """ automatically parametrize Cache.get to int """
        data = self._redis.get(key)
        try:
            data = int(value.decode("utf-8"))
        except Exception:
            data = 0
        return data

    def get_str(self, data: bytes) -> str:
        """ Convert bytes to str """
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """ Convert bytes to int """
        return int.from_bytes(data, byteorder)
