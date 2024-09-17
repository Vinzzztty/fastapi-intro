import pytest
import requests


def test_greet_endpoints():
    url = "http://127.0.0.1:8000/greet/"
    name = "John"

    response = requests.get(url, params={"name": name})

    assert response.status_code == 200

    assert response.json() == {"message": f"Hello, {name}"}
