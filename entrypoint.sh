#!/bin/bash
set -euo pipefail

if [ "$(id -u)" -eq 0 ]; then
    echo "This script must not be run as root." 1>&2
    exit 1
fi

if [ ${#} -eq 0 ]; then
        echo "[*] Applying DB migrations..."
        python ./manage.py migrate
        echo "[*] Run django server..."
        exec python ./manage.py runserver 0.0.0.0:8000
fi

exec "${@}"