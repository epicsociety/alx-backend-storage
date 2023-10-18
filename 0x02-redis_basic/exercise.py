#!/usr/bin/env python3
""" Write strings to redis"""


import redis
import uuid
from typing import Union


class Cache:
    """ store an instance of the Redis client as a private variable """
    def __init__(self) -> None:
        """ Init method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
