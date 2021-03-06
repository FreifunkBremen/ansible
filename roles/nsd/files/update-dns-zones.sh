#! /usr/bin/env bash

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

DNS_ZONES_FOLDER='/opt/ffhb/dns'

# Check if DNS zones folder exists
if [ ! -d "$DNS_ZONES_FOLDER" ]; then
  echo "${DNS_ZONES_FOLDER} does not exists!" >&2
  exit 1
fi

git -C "$DNS_ZONES_FOLDER" pull

for DNS_ZONE in "${DNS_ZONES_FOLDER}/"*.zone; do
  if ! nsd-checkzone "$(basename "$DNS_ZONE" '.zone')" "$DNS_ZONE"; then
    continue
  fi

  cp "$DNS_ZONE" "/var/lib/nsd/"

  # Reload DNS server configuration
  nsd-control reconfig >/dev/null

  # Reload zone
  nsd-control reload "$(basename "$DNS_ZONE" '.zone')"

  # Notify slaves about changed zones
  nsd-control notify "$(basename "$DNS_ZONE" '.zone')"
done
