"""
Usefull utils for some routine tasks
"""
import requests
from json import loads


def post_request(port, path, json):
    """
    helper function to send post data to service
    returns dict object with info
    """
    return loads(requests.post("http://127.0.0.1:{}/{}".format(port, path), json=json).text)
