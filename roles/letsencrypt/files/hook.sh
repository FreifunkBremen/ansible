#!/usr/bin/env bash

case "$1" in
    deploy_cert)
        systemctl reload apache2
esac

exit 0
