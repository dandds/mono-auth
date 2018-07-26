#!/bin/sh

# Add user and group
addgroup -g "${APP_GID}" -S "${APP_GROUP}"
adduser -u "${APP_UID}" -D -S -G "${APP_GROUP}" "${APP_USER}"

# Ensure socket directory is present and has the correct permissions
mkdir -p "${SOCKET_DIRECTORY}"

chown "${APP_USER}":"${APP_GROUP}" -R "${SOCKET_DIRECTORY}"

chmod 750 "${SOCKET_DIRECTORY}"

apk update
apk upgrade

apk --no-cache add uwsgi
apk --no-cache add uwsgi-python3
apk --no-cache add dumb-init
