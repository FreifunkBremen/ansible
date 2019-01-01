command[ IPv4 ]         = /home/{{ monitoring_user }}/.opt/icinga/libexec/check_ping -4 -H $HOSTADDRESS$ -w 3000.0,80% -c 5000.0,100% -p 1 -t 5
command[ IPv6 ]         = /home/{{ monitoring_user }}/.opt/icinga/libexec/check_ping -6 -H $HOSTADDRESS6$ -w 3000.0,80% -c 5000.0,100% -p 2

state   [ CRITICAL   ] = COUNT(CRITICAL) > 1
state   [ WARNING    ] = COUNT(WARNING) > 0 || COUNT(CRITICAL) > 0
state   [ UNKNOWN    ] = COUNT(UNKNOWN) > 1
