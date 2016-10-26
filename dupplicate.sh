#!/bin/bash

# --------------------------
# Author : Clément Robert
# written october 2016
# --------------------------
# This program copies a base simulation with all its file-tree 
# except the output files

# DEFINITIONS
#----------------------------------------------------------------------

function tailcut {
    #this function removes the last character of $1 if it matches $2
    if [ ${1:(-1)} == $2 ]
    then
        res=${1:0:$((${#1}-1))}
    else
        res=$1
    fi
    echo "$res"    
}


# PARSING
#----------------------------------------------------------------------

base=$(tailcut $1 "/")
target=$(tailcut $2 "/")

echo $base
echo $target


# SYNCHRONIZATION
#----------------------------------------------------------------------

rsync -av --exclude='output/*' --exclude='OAR*' $base/ $target


# AUTO-EDITION of files mentioning their own location
#----------------------------------------------------------------------
# /!\ This part may still be subject to bug corrections

sed -i "s!$base!$target!g" $target/jobs/*oar
sed -i "s!$base!$target!g" $target/input*/*par


# SECURITY
#----------------------------------------------------------------------
# we force the user to change persmissions before they can 
# run the simulation in case there is still something wrong

chmod -x $target/*exe 