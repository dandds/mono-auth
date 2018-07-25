import os
from flask import Flask, request, redirect, make_response

app = Flask(__name__)
secret = os.urandom(24).hex()


# This is just here so that there is a root route.
@app.route("/")
def root():
    return "Hello, this is the root page."


# This is a stand-in for the user login page with the "Sign in" buttons.
@app.route("/login")
def login():
    return "Pretend this page has login buttons. Go to https://dev.cac.atat.codes/cac-login."


# This is the only protected route in the demo. It checks for the existence of
# the session cookie, and redirects to the login page if it doesn't exist.
@app.route("/protected")
def protected():
    cookie = request.cookies.get("mono-auth")
    if cookie and cookie == secret:
        return "you got here i guess"

    else:
        return redirect("/login")


# Not protected. Just a generic error page for when authentication fails.
@app.route("/error")
def error():
    return "authentication failed!"


# This is the endpoint that would be responsible for the heavy lifting. It is
# available at https://dev.cac.atat.codes/cac-login.
# If client authentication is successful, it redirects you to the /protected
# route. If not, it redirects to /error.
# If this were the real app, it would:
#     - perform the CRL check
#     - check if the user exists in the database and create it if not
#     - create a new user session
#     - assign a session cookie
@app.route("/cac-login")
def cac_login():
    if request.environ.get("HTTP_X_SSL_CLIENT_VERIFY") == "SUCCESS":
        resp = make_response(redirect("/protected"))
        # This is like a session.
        resp.set_cookie(
            "mono-auth", secret, domain=".atat.codes", httponly=True, secure=True
        )
        return resp

    else:
        return redirect("/error")
