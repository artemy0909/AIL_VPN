import requests
from yarl import URL

from utils.callback_stored import CallbackCache


class XenonConnectionError(ConnectionError):
    pass


def benchmark(func):
    from datetime import datetime

    def wrapper(*args, **kwargs):
        t = datetime.now()
        res = func(*args, **kwargs)
        print(func.__name__, datetime.now() - t)
        return res

    return wrapper


def _request(func):
    def wrapper(*args, **kwargs):
        for key, value in kwargs.items():
            if isinstance(value, CallbackCache):
                kwargs[key] = value.model_dump(mode="json")
        response = func(*args, json=kwargs)
        if not response.ok:
            raise XenonConnectionError(
                f"The server returned an error code {response.status_code} ({response.reason})"
                f"{f': {response.text}' if response.status_code == 500 else ''}")
        else:
            return response

    return wrapper


class XenonClient:

    def __init__(self, api_url, login, password):
        self.api_url = URL(api_url)
        self.session = requests.Session()
        self.session.auth = (login, password)

    def test(self):
        self.get("echo")

    @_request
    def get(self, method_name, **kwargs):
        return self.session.get(self.api_url / method_name, **kwargs)

    @_request
    def post(self, method_name, **kwargs):
        return self.session.post(self.api_url / method_name, **kwargs)

    @_request
    def put(self, method_name, **kwargs):
        return self.session.put(self.api_url / method_name, **kwargs)
