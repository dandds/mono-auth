import os
from flask import Flask, request, redirect, make_response

app = Flask(__name__)
secret = os.urandom(24).hex()


@app.route("/")
def root():
    return "Hello, this is the root page."


@app.route("/login")
def login():
    return "Pretend this page has login buttons. Go to https://dev.cac.atat.codes/cac-login."


@app.route("/protected")
def protected():
    cookie = request.cookies.get("mono-auth")
    if cookie and cookie == secret:
        return "you got here i guess"

    else:
        return redirect("/login")


@app.route("/error")
def error():
    return "authentication failed!"


@app.route("/cac-login")
def cac_login():
    if request.environ.get("HTTP_X_SSL_CLIENT_VERIFY") == "SUCCESS":
        resp = make_response(redirect("/protected"))
        # this is like a session
        resp.set_cookie(
            "mono-auth", secret, domain=".atat.codes", httponly=True, secure=True
        )
        return resp

    else:
        return redirect("/error")

