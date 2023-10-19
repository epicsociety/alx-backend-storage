#!/usr/bin/env python3
""" Write strings to redis"""


import redis
import uuid
from typing import Union, Callable
import functools


def count_calls(method):
    """ implement a system to counting"""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method):
    """
    store the history of inputs and outputs for a particular function
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(inputs_key, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(outputs_key, str(output))

        return output
    return wrapper


class Cache:
    """ store an instance of the Redis client as a private variable """
    def __init__(self) -> None:
        """ Init method """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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


def replay(method):
    """ display the history of calls of the function store"""
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")

    for args, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{args.decode()}) -> {output.decode()}")


cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)

replay(cache.store)
