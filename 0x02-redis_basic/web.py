#!/usr/bin/env python3
"""
Web caching and tracking module using Redis.
"""

import redis
import requests
from typing import Callable
from functools import wraps


def track_access(method: Callable) -> Callable:
    """
    Decorator to track the number of times a URL is accessed.

    Args:
        method: The method to wrap.

    Returns:
        The wrapped method.
    """
    @wraps(method)
    def wrapper(url: str, *args, **kwargs):
        """
        Wrapper to increment the count of URL accesses.
        """
        count_key = f"count:{url}"
        wrapper.redis_instance.incr(count_key)
        return method(url, *args, **kwargs)

    wrapper.redis_instance = redis.Redis()
    return wrapper


class WebCache:
    """
    WebCache class to handle URL caching and tracking.
    """

    def __init__(self):
        """
        Initialize Redis connection.
        """
        self._redis = redis.Redis()

    @track_access
    def get_page(self, url: str) -> str:
        """
        Fetch and cache a webpage's content.

        Args:
            url: The URL to fetch.

        Returns:
            The HTML content of the URL.
        """
        cache_key = f"cache:{url}"
        cached_content = self._redis.get(cache_key)

        if cached_content:
            return cached_content.decode("utf-8")

        # Fetch and cache the content with 10-second expiration
        response = requests.get(url)
        html_content = response.text
        self._redis.setex(cache_key, 10, html_content)
        return html_content

    def get_access_count(self, url: str) -> int:
        """
        Get the access count of a URL.

        Args:
            url: The URL to check.

        Returns:
            The number of times the URL has been accessed.
        """
        count_key = f"count:{url}"
        count = self._redis.get(count_key)
        return int(count) if count else 0

