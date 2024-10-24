#!/bin/bash

export PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin

# Full path to sshpass and scp
SSH_PASS=/usr/bin/sshpass
SCP=/usr/bin/scp

#sshpass -p "nowcast@bppt" scp swirls@10.41.16.131:/home/swirls/data_gfs/swmi/u850_`date -d yesterday +%\Y%\m%\d`_gfs_gefs_00z ./gefs
sshpass -p "nowcast@bppt" scp swirls@10.41.16.131:/home/swirls/data_gfs/swmi/u850_$(date -d yesterday +%Y%m%d)_gfs_gefs_00z /home/diong/Desktop/SWMI2/gefs
