#!/usr/bin/env bash

case "$1" in
    deploy_challenge)
        ;;
    clean_challenge)
        ;;
    deploy_cert)
        systemctl reload apache2
        if [ -d /etc/.git ]; then
            cd "$(dirname "$3")"
            git add .
            git commit -m "letsencrypt: refreshed certificate for $2" .
        fi
        ;;
    unchanged_cert)
        ;;
    *)
        echo "Unknown hook $1"
        exit 1
        ;;
esac

exit 0
