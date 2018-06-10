#!/bin/sh

#
# Creates backup of entire webserver using Restic.
#
# Selected data is excluded from backup.
#
# Parameters:
# 1: target repository (ie. the "-r" parameter for restic)
# 2: path to password file (full path to file containing the repository password)
#

repository=$1
passwordFile=$2

restic \
    --repo "$repository" \
    --password-file "$passwordFile" \
    --one-file-system \
    --quiet \
    --exclude=/var/www/downloads/domains/downloads.bremen.freifunk.net/ \
    --exclude=/var/log/journal/ \
    --exclude="/home/tiles/*.mbtiles" \
    --exclude="/home/tiles/*.mbtiles3" \
    --exclude=/var/lib/grafana/png/ \
    --exclude=/var/lib/influxdb/ \
    --exclude=/var/cache/ \
    --exclude=/root/.cache/ \
    --exclude="/home/*/.cache" \
    --exclude=/tmp/ \
    --exclude=/var/tmp/ \
    backup /
