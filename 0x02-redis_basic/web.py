#!/usr/bin/env python3
"""
Module to implement an expiring web cache and tracker using Redis.
This script provides functionality to cache web pages and track the number of
times they are accessed.
"""

import requests
import redis
from functools import wraps
from typing import Callable

redis_client = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    A decorator that counts the number of times a URL has been requested.
    Args:
    method (Callable): The function to be decorated.

    Returns:
    Callable: The decorated function.
    """
    @wraps(method)
    def wrapper(url):
        count_key = f"count:{url}"
        redis_client.incr(count_key)

        cache_key = f"cached:{url}"
        cached_content = redis_client.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')

        html_content = method(url)
        redis_client.setex(cache_key, 10, html_content)
        return html_content
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Fetches the HTML content of a given URL.
    Args:
    url (str): The URL from which to fetch content.

    Returns:
    str: The HTML content of the page.
    """
    response = requests.get(url)
    return response.text
