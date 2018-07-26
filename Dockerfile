FROM python:3.6.5-alpine

RUN pip install --upgrade pip
RUN pip install pipenv

COPY ./ /app
WORKDIR /app/
RUN pipenv install --system --deploy --ignore-pipfile

RUN mkdir /var/log/uwsgi

EXPOSE 80 443
