"""
Usefull utils for some routine tasks
"""
import time
from json import loads

import requests


def post_request(port, path, json):
    """
    Helper function to send post data to service
    returns dict object with info
    """
    return loads(requests.post("http://127.0.0.1:{}{}".format(port, path),
                               json=json).text)


def timed(func):
    """
    Decorator for time checking of function
    """
    def decorate(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('{}: {}'.format(func.__name__, time.time() - start))
        return res
    return decorate
