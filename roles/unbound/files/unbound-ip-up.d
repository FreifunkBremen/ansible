#! /usr/bin/env bash

PATH=/sbin:/usr/sbin:/bin:/usr/bin

if ! pgrep unbound >/dev/null 2>&1; then
  service unbound restart
fi

exit 0
