"""
Wrapper of hello in python for testing
Provides utilites to
1. setup server
2. get response form server
3. teardown server
"""
import os
import urllib.request


def setup_server(port=None):
    if port:
        print(f"Running server on {port}")
        os.system(f'./hello -addr :{port} &')
    else:
        print(f"Running server on 8080")
        os.system(f'./hello &')


def get_respose(url):
    with urllib.request.urlopen(url) as response:
        return response.code, response.read()


def kill_server(port):
    """
    TODO: Implement kill server
    """
    pass