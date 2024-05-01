#!/usr/bin/env python3
"""
Module containing the Cache class for storing and retrieving
data from a Redis database using randomly generated keys.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method of the Cache class is
    called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs of a method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        # Serialize the inputs and append to Redis list
        inputs_key = f"{method.__qualname__}:inputs"
        self._redis.rpush(inputs_key, str(args))

        # Call the function and store the output
        output = method(self, *args, **kwargs)
        outputs_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(outputs_key, str(output))

        return output
    return wrapper


class Cache:
    """
    Cache class that handles storage and retrieval of data in Redis.
    """
    def __init__(self):
        """
        Initialize the Redis client and flush any existing data in the
        database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the given data in Redis using a random key.

        Args:
            data (Union[str, bytes, int, float]): The data to store in Redis.

        Returns:
            str: The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(name=key, value=data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> \
            Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis by key, optionally applying a conversion
        function.

        Args:
            key (str): The Redis key under which the data is stored.
            fn (Optional[Callable]): A function to convert the data from bytes
                                     to the desired format (default is None,
                                     which returns the data as bytes).

        Returns:
            Union[str, bytes, int, float, None]: The data retrieved from Redis,
                                                 possibly converted to a
                                                 different type, or None if the
                                                 key does not exist.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis.

        Args:
            key (str): The Redis key.

        Returns:
            Optional[str]: The string data or None if key does not exist.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.

        Args:
            key (str): The Redis key.

        Returns:
            Optional[int]: The integer data or None if key does not exist.
        """
        return self.get(key, int)
