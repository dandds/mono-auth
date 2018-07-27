FROM nginx:alpine

ARG APP_UID=9650
ARG SOCKET_DIRECTORY=/var/run/uwsgi

ENV APP_UID "${APP_UID}"
ENV SOCKET_DIRECTORY "${SOCKET_DIRECTORY}"

COPY ./script /app/script
COPY ./ssl /app/ssl
COPY ./atat.nginx.conf /etc/nginx/conf.d/atat.nginx.conf

RUN /app/script/setup_nginx.sh

# Use dumb-init for proper signal handling
ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# Launch nginx
CMD ["nginx", "-g", "daemon off;"]

EXPOSE 80 443
