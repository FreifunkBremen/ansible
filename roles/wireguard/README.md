# Install

## Configurate
```
[Interface]
Table      = off
PrivateKey = {{OWN_PRIVATE_KEY}}
ListenPort = 40000
Address    = fe80::9:2/64
PostUp     = ip l set multicast on dev %i

[Peer]
PublicKey  = hCQLda2ABtuAXrYThdYr47hig0NRvY+5+NBIE5a+xDg=
AllowedIPs = ::/0
EndPoint   = vpn04.bremen.freifunk.net:40{{PORT}}

```

make run on boot: `systemctl enable wg-quick@wg-bb-up.service`

start wireguard connection: `systemctl start wg-quick@wg-bb-up.service`

## Example Firewall
```
# wireguard tunnel
ipt -A INPUT -p udp -m multiport --dports 40000:40100 -j ACCEPT

# forwarding between wireguard interfaces
ipt6 -A FORWARD -o wg-bb-+ -i babel-wg+ -j ACCEPT
ipt6 -A FORWARD -i wg-bb-+ -o babel-wg+ -j ACCEPT
ipt6 -A FORWARD -o wg-bb-+ -i wg-bb-+ -j ACCEPT

# respondd (with mmfd + mesh-announce)
ipt6 -A INPUT -i wg-bb-+ -p udp --dport 1001 -j ACCEPT

```
