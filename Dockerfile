FROM tiangolo/uwsgi-nginx:python3.6

RUN pip install --upgrade pip
RUN pip install pipenv

COPY ./ /app
WORKDIR /app/
RUN pipenv install --system --deploy --ignore-pipfile

RUN mkdir /var/log/uwsgi

RUN ln -s /app/atat.nginx.conf /etc/nginx/conf.d/

EXPOSE 80 443
