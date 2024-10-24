#!/bin/bash

source /home/`whoami`/bash_profile

source /home/`whoami`/.bashrc

cd /home/`whoami`/Desktop/SWMI2/

   python SWMI2_diong1.py

   cd ./test/

   sshpass -p 'paraset' scp -rv  GEFS_SWMI2.png KC@10.41.16.134:/var/www/html/ideas/southwest_monsoon

cd 


#export PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin

#python /home/diong/Desktop/SWMI2/SWMI2_diong.py
#sshpass -p 'paraset' scp -v -r -t ./test/GEFS_SWMI2.png KCS@10.41.16.134://var/www/html/ideas/southwest_monsoon
#sshpass -p 'paraset' scp -v -r  home/diong/Desktop/SWMI2/test/GEFS_SWMI2.png KC@10.41.16.134://var/www/html/ideas/southwest_monsoon
