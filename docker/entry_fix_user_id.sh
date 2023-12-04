#!/bin/bash
# Fixes the docker user UID/GID to match the host UID/GID. This helps avoid
# annoying issues where the docker user can't modify the host user's file and
# vice-versa (i.e. make and make-clean).

if [[ -n "${DOCKER_UID}" ]] && [[ -n "${DOCKER_GID}" ]]; then
    if [[ "${DOCKER_UID}" -ne 1000 ]] || [[ "${DOCKER_GID}" -ne 1000 ]]; then
        groupmod --gid="${DOCKER_GID}" user
        usermod --uid="${DOCKER_UID}" --gid="${DOCKER_GID}" user
        chown --recursive user:user /home/user
    fi
    exec /usr/sbin/gosu user "$@"
fi

exec "$@"
