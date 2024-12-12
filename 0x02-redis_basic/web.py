#!/usr/bin/env python3
"""
Web caching and tracking module using Redis.
"""

import redis
import requests
from typing import Callable

class Cache:
    """
    Cache class for web content caching and access tracking.
    """

    def __init__(self):
        """
        Initialize Redis connection.
        """
        self._redis = redis.Redis()

    def get_page(self, url: str) -> str:
        """
        Retrieve a web page and cache it.

        Args:
            url: The URL to fetch.

        Returns:
            The HTML content of the page.
        """
        # Check if the URL is cached
        cache_key = f"cache:{url}"
        cached_content = self._redis.get(cache_key)
        if cached_content:
            return cached_content.decode("utf-8")

        # Fetch the content if not cached
        response = requests.get(url)
        html_content = response.text

        # Cache the content with expiration time of 10 seconds
        self._redis.setex(cache_key, 10, html_content)

        # Increment access count
        count_key = f"count:{url}"
        self._redis.incr(count_key)

        return html_content

    def get_access_count(self, url: str) -> int:
        """
        Get the access count of a URL.

        Args:
            url: The URL to check.

        Returns:
            The number of times the URL was accessed.
        """
        count_key = f"count:{url}"
        count = self._redis.get(count_key)
        return int(count) if count else 0

