#!/bin/sh

set -eu

RULEPATH="${RULEPATH:-"{{ firewall_path }}"}"

new_rule() {
	for arg in "$@"; do
		case "$arg" in
		-I|-A)
			comment="Set by file $rule"
			;;
		--comment)
			comment=""
			break
			;;
		esac
	done

	"$@" ${comment:+-m comment --comment "${comment}"} \
		|| echo "$@" ${comment:+-m comment --comment "${comment}"}
}

ipt() {
	ipt4 "$@"
	ipt6 "$@"
}

ipt4() {
	new_rule iptables "$@"
}

ipt6() {
	new_rule ip6tables "$@"
}

case "$1" in
start|restart)
	for rule in "$RULEPATH"/*; do
		. "$rule"
	done
	;;
*)
	echo "Action $1 unsupported"
esac