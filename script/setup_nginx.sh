#!/bin/sh

# Ensure socket directory is present and has the correct permissions
mkdir -p "${SOCKET_DIRECTORY}"

# Update nginx user uid



apk update
apk upgrade
apk --no-cache add shadow
apk --no-cache add dumb-init

usermod -u "${APP_UID}" nginx

chown -R nginx "${SOCKET_DIRECTORY}"
chmod 750 "${SOCKET_DIRECTORY}"
