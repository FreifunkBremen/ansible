#!/bin/sh

#
# Prepares data for backup
#
#
# Currently this means:
# - export InfluxDB data into backup format
#
# The prepared data can then be backed up easily.
#


# create backup of InfluxDB:
rm -rf /var/backups/influxdb/
influxd backup -portable /var/backups/influxdb/ >/dev/null
# unpack backup, for better deduplication by Restic:
for f in /var/backups/influxdb/*.tar.gz; do
	gunzip "$f"
done


# TODO: also create backup of MySQL data
