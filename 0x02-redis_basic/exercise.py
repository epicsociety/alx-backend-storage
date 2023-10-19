#!/usr/bin/env python3
""" Write strings to redis"""


import redis
import uuid
from typing import Union, Optional, Callable


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

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:  # noqa: E501
        """
        Convert the data back to the desired format.
        Args:
            key: str
            fn: callable
        Returns: converted data
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Parametrize Cache.get with the correct conversion function"""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """"Parametrize Cache.get with the correct conversion function"""
        return self.get(key, fn=int)
