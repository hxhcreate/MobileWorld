#!/bin/bash

# disable ipv6 otherwise sim card will be disabled in android emulator
# related issue: https://issuetracker.google.com/issues/215231636?pli=1
sysctl net.ipv6.conf.all.disable_ipv6=1
# located at /usr/local/bin/start-docker.sh
start-docker.sh


cd /app/images
for f in *.tar; do docker load -i "$f"; done

cd /app/service


if [ "${ENABLE_VNC:-false}" = "true" ] || [ "${ENABLE_VNC:-false}" = "1" ]; then
    /app/docker/start_novnc.sh
    # assuming dev mode
    uv sync --extra dev --no-cache
else
    uv run mobile-world viewer --port 7860 &
fi
/app/docker/start_emulator.sh

uv run mobile-world server --port 6800 >> /var/log/server.log 2>&1 &

# Execute specified command
"$@"