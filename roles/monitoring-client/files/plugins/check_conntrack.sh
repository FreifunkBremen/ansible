#! /bin/bash
#
# check_netfilter.nf_conntrack.sh nagios plugin
#
# by Jeronimo Zucco <jczucco+nagios@gmail.com>
# April/20/2012
#
# This Nagios plugin was created to check the status of netfilter conntrack table
#
# sysctl net.netfilter.nf_conntrack_count : check the number of connections in table
# sysctl net.netfilter.nf_conntrack_max : check the max size of netfilter conntrack table
#
# Licence: "GNU Public License v2"
# Dependencies: expr, grep, sed
#
# If you are running a Linux firewall, you should be using this script ;-)
# 
# nagiosgraph map:
# /output:Conntrack Tables.*?(\d+)\n/
# and push @s, [ 'conntrack',
#                [ 'entries', GAUGE, $1 ] ];


PROGNAME=`basename $0`
PROGPATH=`echo $0 | sed -e 's,[\\/][^\\/][^\\/]*$,,'`
REVISION="0.1"
PATH="$PATH:/sbin"

. /usr/lib/nagios/plugins/utils.sh


print_usage() {
  echo "Usage:"
  echo "  $PROGNAME WARNING% CRITICAL%"
  echo "  $PROGNAME --help"
  echo "  $PROGNAME --version"
}

print_help() {
  print_revision $PROGNAME $REVISION
  echo ""
  print_usage
  echo ""
  echo "Check netfilter conntrack table status"
  echo ""
  echo "The percs are based in net.netfilter.nf_conntrack_max and net.netfilter.nf_conntrack_count"
  echo ""
  echo "--help"
  echo "   Print this help screen"
  echo "--version"
  echo "   Print version and license information"
}

if [ $# -eq 2 ]
then
	USED=$(sysctl -n net.netfilter.nf_conntrack_count)
	MAX=$(sysctl -n net.netfilter.nf_conntrack_max)

	WARNING=$(echo $1 | sed s/%//)
	CRITICAL=$(echo $2 | sed s/%//)

	if [ ${MAX} -gt 0 ]; then
		AUX=$(expr ${USED} \* 100 / ${MAX} )

                if [ ${AUX} -lt ${WARNING} ]; then
                        echo "Conntrack Tables OK - ${USED}|con=${USED}"
                        exit $STATE_OK
                else
                        if [ ${AUX} -ge ${CRITICAL} ]; then
				echo "Conntrack Tables CRITICAL - ${USED}|con=${USED}"
                                exit $STATE_CRITICAL
                        else
                                if [ ${AUX} -ge ${WARNING} ]; then
					echo "Conntrack Tables WARNING - ${USED}|con=${USED}"
                                        exit $STATE_WARNING
                                fi
                        fi
                fi
	else 
                echo "Can't check net.netfilter.nf_conntrack_max"
		exit $STATE_WARNING
        fi


else
	case $1 in
		--help)
                	print_help
    			exit $STATE_OK
    			;;
		--version)
                	print_revision $PROGNAME $REVISION
    			exit $STATE_OK
    			;;
		*)
    			print_usage
    			exit $STATE_OK
			;;
	esac
fi
