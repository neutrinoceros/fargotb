#!/bin/bash

# This program intends to copy a base simulation with all its filetree 
# but rejects the outputs
#
# known issue : automatic replacement of dir name in files may not work
#               if the user provides $base ending with a "/" character
base=$1
target=$2

rsync -av --exclude='output/*' --exclude='OAR*' $base/ $target

sed -i "s!$base!$target!g" $target/jobs/*oar
sed -i "s!$base!$target!g" $target/input*/*par

# security : we force the user to change persmissions before they can run the simulation in case there is still something wrong
chmod -x $target/*exe 