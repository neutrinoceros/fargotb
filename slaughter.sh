#!/bin/bash
#
# --------------------------
# Author : Clément Robert
# written october 2016
# --------------------------
# This program politely asks if you really wish it 
# to kill *all* your simulations, then does.
#
# It accepts the argument "picky" (-p|-P|--picky) followed by a string.
# In this case, it will only kill jobs whose descriptive line in 
# oartstat matches this string.

# PARSING
#----------------------------------------------------------------------

GREPING="grep $USER"

while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -p|-P|--picky)
        target="$2"
        GREPING="$GREPING | grep $target"
        shift
        ;;
    *)
        ;;
esac
shift
done

jobs=$(oarstat | eval $GREPING | tr -s ' ' \
    | awk '{gsub(" *.*=","",$5); printf "%7s  %10s  %30s\n",$1,$4,$5}')


tokill=$(eval """echo "$jobs" |  cut -d ' ' -f 1""")


# PROCEDURE
#----------------------------------------------------------------------

echo "You are about to kill the following jobs :"
echo "    num     runtime                              id"
echo "-----------------------------------------------------------"
echo -e "$jobs\n" 
read -p "proceed (y/[n])?    " choice

case "$choice" in
    y|Y|yes|YES ) for jobnumber in ${tokill[*]}
        do oardel $jobnumber; done 
	;;
    *) echo "I'm sorry Dave. I'm afraid I can't do that"
        ;;
esac