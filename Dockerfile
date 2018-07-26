FROM python:3.6.5-alpine

ARG APP_USER=uwsgi
ARG APP_UID=9650
ARG APP_GROUP=atat
ARG APP_GID=9650
ARG SOCKET_DIRECTORY=/var/run/uwsgi

ENV APP_USER "${APP_USER}"
ENV APP_UID "${APP_UID}"
ENV APP_GROUP "${APP_GROUP}"
ENV APP_GID "${APP_GID}"
ENV SOCKET_DIRECTORY "${SOCKET_DIRECTORY}"
ENV PYTHONPATH=/usr/local/lib/python3.6/site-packages

RUN mkdir /var/log/uwsgi

RUN pip install --upgrade pip
RUN pip install pipenv

COPY ./script /script

RUN /script/setup_app.sh

COPY ./ /app

WORKDIR /app/
RUN pipenv install --system --deploy --ignore-pipfile
RUN chown -R "${APP_USER}":"${APP_GROUP}" /app

USER "${APP_USER}"

# Use dumb-init for proper signal handling
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Default command is to run all the tests
CMD ["sh", "-c", "uwsgi --ini ./uwsgi.ini.container"]
