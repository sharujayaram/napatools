#!/bin/bash
hostname=$(hostname -I | awk '{print $1}')
echo $hostname
hostip="${hostname//./_}"
nohup vmstat 2 1000 > /root/sharath/napatools/mongotools/vmstat_$hostip.log &

