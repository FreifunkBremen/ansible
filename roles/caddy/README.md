# caddy

## Bugfix
Caddy need the current version of systemd (or without user change)

```
deb http://httpredir.debian.org/debian jessie-backports main contrib non-free
```

```
apt update
apt install systemd -t jessie-backports
apt upgrade -t jessie-backports
```
