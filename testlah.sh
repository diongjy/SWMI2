#!/bin/bash
source ~/.bashrc

HOST="10.41.16.131"
USERNAME="swirls"
PASSWORD="nowcast@bppt"

#Remote directory to download
REMOTE_DIR="u850_`date -d yesterday +%Y%m%d`_gfs_gefs_00z"

LOCAL_DIR="./gefs"

LOG_FILE="./download_log.txt"

#COnnect to the remote server and download data

lftp <<EOF
debug
open $HOST
user $USERNAME $PASSWORD
cd data_gfs
cd swmi
get u850_`date -d yesterday +%Y%m%d`_gfs_gefs_00z -o ./gefs
#mirror --verbose --use-pget-n=8 --log=$LOG_FILE $REMOTE_DIR $LOCAL_DIR

bye
EOF

#sshpass -p "nowcast@bppt" scp swirls@10.41.16.131:/home/swirls/data_gfs/swmi/u850_`date -d yesterday +%Y%m%d`_gfs_gefs_00z /home/diong/Dekstop/SWMI2/gefs
