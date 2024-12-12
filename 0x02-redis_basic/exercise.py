#!/usr/bin/env python3
"""
Module for basic Redis operations.
"""

import redis
from typing import Union, Callable
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of calls to a method.

    Args:
        method: The method to wrap.

    Returns:
        The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to count and call the original method.
        """
        key = f"{method.__qualname__}"
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of calls to a method.

    Args:
        method: The method to wrap.

    Returns:
        The wrapped method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function to store inputs and outputs in Redis.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store inputs
        self._redis.rpush(input_key, str(args))

        # Call the original method
        output = method(self, *args, **kwargs)

        # Store outputs
        self._redis.rpush(output_key, str(output))
        return output

    return wrapper


def replay(method: Callable):
    """
    Display the history of calls to a particular method.

    Args:
        method: The method whose history to display.
    """
    redis_instance = method.__self__._redis
    input_key = f"{method.__qualname__}:inputs"
    output_key = f"{method.__qualname__}:outputs"

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(inputs)} times:")

    for inp, out in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{inp.decode('utf-8')})
                -> {out.decode('utf-8')}")


class Cache:
    """
    Cache class for interacting with Redis.
    """

    def __init__(self):
        """
        Initialize Redis connection and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis and return a unique key.

        Args:
            data: The data to store (str, bytes, int, or float).

        Returns:
            A string key associated with the stored data.
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None)
    -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally convert it.

        Args:
            key: The key to look up.
            fn: A function to convert the data.

        Returns:
            The retrieved data, optionally converted using fn.
        """
        data = self._redis.get(key)
        return fn(data) if fn and data else data

    def get_str(self, key: str) -> str:
        """
        Retrieve data as a string.

        Args:
            key: The key to look up.

        Returns:
            The retrieved data as a string.
        """
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """
        Retrieve data as an integer.

        Args:
            key: The key to look up.

        Returns:
            The retrieved data as an integer.
        """
        return self.get(key, int)
