#!/bin/bash
#
# --------------------------
# Author : Clément Robert
# written october 2016
# --------------------------
# This program politely asks if you really wish it 
# to kill *all* your simulations, then does.


# PARSING
#----------------------------------------------------------------------

jobs=$(oarstat | grep $USER)
tokill=$(echo $jobs |cut -d ' ' -f 1)


# PROCEDURE
#----------------------------------------------------------------------

echo "You are about to kill the following jobs :"
echo -e "\n$jobs\n" 
read -p "proceed (y/[n])?    " choice
case "$choice" in
    y|Y|yes|YES ) oardel $tokill;;
    *) echo "I'm sorry Dave. I'm afraid I can't do that";;
esac