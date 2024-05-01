#!/usr/bin/env python3
"""
Module containing the Cache class for storing and retrieving
data from a Redis database using randomly generated keys.
"""

import redis
import uuid
from typing import Union


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
