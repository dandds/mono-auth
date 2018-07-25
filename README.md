# ATAT Monolith CAC Auth Demo

This repo contains a small demo of how to handle CAC auth in a monolith architecture. In order to do CAC authentication on a single endpoint within the app, we need a slightly more complicated NGINX setup to allow for two different kinds of SSL termination (regular server SSL and mutual--client and server--SSL).

The basic idea is that we have NGINX configuration for two separate subdomains. In this case, dev.cac.atat.codes (for authentication) and app.atat.codes (for everything else). Both proxy to the _same_ Flask app.

The authentication domain will only accept requests to the endpoint set up for auth (`/cac-login`, in the demo). Every other request to the authentication domain redirects to the everything-else domain. If a user successfully authenticates, we set a domain-level session cookie and redirect them to their home screen on the everything-else domain.

The everything-else domain has a protected route, `/protected`. This is a stand-in for most of the ATAT app, which will be protected. If a user hits that endpoint without a session cookie, they will be redirected to a login screen.

## Run the Demo

### Edit /etc/hosts

For this to work, you need to add the following to your `/etc/hosts` file:

```
127.0.0.1 dev.cac.atat.codes
127.0.0.1 app.atat.codes
```

You'll probably need to edit the file as root. This sets your DNS for those two domains to localhost.

### Set up the docker container and run the tests

```
pipenv install
docker-compose up --build -d
pipenv run pytest
```

The tests illustrate the full workflow.

If you have a smart card reader and a valid card, you can try going to https://dev.cac.atat.codes/cac-login. If your authentication is successful, you will be redirect to https://app.atat.codes/protected.

If you don't have a smart card reader and card, you can play around with hitting the different routes in the Flask app. If you try to hit any endpoint on https://dev.cac.atat.codes, you will be redirected to its https://app.atat.codes equivalent. The exception to this is https://dev.cac.atat.codes/cac-login, where the client authentication happens. If you visit that URL without a valid smart card, you will be redirect back to https://app.atat.codes/error.

The tests outline the authentication workflow in detail and the endpoint in the Flask app (`mono_app/app.py`) contain some further explanation.
