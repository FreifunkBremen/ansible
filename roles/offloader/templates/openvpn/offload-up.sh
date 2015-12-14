#!/bin/bash
brctl addif {{main_bridge}} {{offload_interface}}

ip link set {{offload_interface}} up
