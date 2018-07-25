import os
import re
import pytest
import requests
import urllib3
from test.helpers import is_token, relative_dir


@pytest.fixture
def server_api():
    host = os.getenv("SERVER_NAME")
    server_name = f"https://{host}"
    return server_name


@pytest.fixture
def client():
    ct = requests.Session()
    ct.verify = False
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    return ct


VALID_CERTS = (
    relative_dir("ssl/client-certs/atat.mil.crt"),
    relative_dir("ssl/client-certs/atat.mil.key"),
)


def test_protected_route(client):
    resp = client.get("https://app.atat.codes/protected", allow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["Location"] == "https://app.atat.codes/login"


def test_login_without_cac(client):
    resp = client.get("https://dev.cac.atat.codes/cac-login")
    assert "authentication failed" in resp.text
    assert resp.url == "https://app.atat.codes/error"


# do not follow redirect, do it ourselves
def test_no_redirect_log_in_with_cac(client):
    resp = client.get(
        "https://dev.cac.atat.codes/cac-login", cert=VALID_CERTS, allow_redirects=False
    )
    assert resp.status_code == 302
    assert len(client.cookies) == 1
    resp = client.get("https://app.atat.codes/protected", allow_redirects=False)
    assert resp.status_code == 200


# follow redirect, do it ourselves
def test_redirect_log_in_with_cac(client):
    resp = client.get(
        "https://dev.cac.atat.codes/cac-login", cert=VALID_CERTS
    )
    assert resp.status_code == 200
    assert resp.url == "https://app.atat.codes/protected"
