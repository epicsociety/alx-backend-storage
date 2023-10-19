#!/usr/bin/env python3
"""
obtain the HTML content of a particular URL and returns it using requests
"""

import requests
import redis
import time

# Connect to Redis
redis_client = redis.Redis()


def count_accesses(url):
    """how many times the URL was accessed """
    def decorator(func):
        """ decorator"""
        def wrapper(*args, **kwargs):
            """Increment the access count for this URL"""
            access_count_key = f"count:{url}"
            redis_client.incr(access_count_key)
            return func(*args, **kwargs)
        return wrapper
    return decorator


@count_accesses(url)
def get_page(url):
    """ Check if the response is cached """
    cache_key = f"cache:{url}"
    cached_response = redis_client.get(cache_key)

    if cached_response:
        print(f"Using cached response for {url}")
        return cached_response.decode('utf-8')

    # Make a request to the URL
    response = requests.get(url)

    # Cache the response with an expiration time of 10 seconds
    redis_client.setex(cache_key, 10, response.text)

    return response.text


url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
html_content = get_page(url)
print(html_content)

# Simulate accessing the same URL multiple times
for _ in range(3):
    html_content = get_page(url)
    print(html_content)
