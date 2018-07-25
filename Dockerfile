FROM tiangolo/uwsgi-nginx:python3.6

RUN pip install --upgrade pip
RUN pip install pipenv

COPY ./ /app
WORKDIR /app/
RUN pipenv install --system --deploy --ignore-pipfile

RUN mkdir /var/log/uwsgi

COPY ssl/*.conf /etc/nginx/conf.d/
COPY ssl/server-certs/ /etc/ssl/

EXPOSE 80 443
