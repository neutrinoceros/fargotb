#!/bin/bash

# --------------------------
# Author : Clément Robert
# written october 2016
# --------------------------
# This program generates an append-chain of jobs based on the first one, 
# matching the number of outputs in numerical_config.par

# DEFINITIONS
#----------------------------------------------------------------------

inputfile=$1

function parser { 
cat $1 | grep -i $2 | tr -s ' ' | cut -d ' ' -f 2
}


# PARSING
#----------------------------------------------------------------------

# read the input file displaying all necessary information
simdir=$(parser $inputfile simdir)
configdir=$simdir/$(parser $inputfile configdir)
jobsdir=$simdir/$(parser $inputfile jobsdir)
seedjob=$jobsdir/$(parser $inputfile seedjob)

configfile=$configdir/$(parser $inputfile configfile)
OPD=$(parser $inputfile OPD)

# go into the configuration file to grasp more details
ninterm=$(parser $configfile ninterm)
ntot=$(parser $configfile ntot)

# conversion into usable variables
OPD=$(printf "%.f" $OPD)
ninterm=$(printf "%.f" $ninterm)
ntot=$(printf "%.f" $ntot)
seed="${seedjob%.*}"          # seed is now identical to seejob except 
                              # that it does not contain the extension

# computation
#/////////////////////////////////////////////////////////
# /!\ security : temp, should be deleted in future version
OPD=$(($OPD-1))
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

NJ=$(($ntot/($OPD*$ninterm))) # number of jobs recquiered by the user


# MAIN LOOP
#----------------------------------------------------------------------

i=1

# create and edit the new jobs
cd $simdir
while [ $i -le $NJ ]
do
    newfile=$seed\_$i.oar
    restart=$(($OPD*$i))
    cp $seedjob $newfile
    sed -i "s/\$EXECUTABLE/\$EXECUTABLE -s $restart/g" $newfile
    # DANGER AHEAD
    #//////////////////////////////////////////////////
    if [ $i -eq 1 ] 
    then
        oarsub -S $newfile
    fi

    if [ $i -gt 1 ]
    then
        # get the number of the previousjob
        jobnumber=$(oarstat | grep $USER | tail -1 | cut -d ' ' -f 1)
        # submit the newjob, as an appendage of the previous one
        oarsub -S -a $jobnumber $newfile
    fi
    # END OF DANGER ZONE
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    i=$(($i+1))
done
cd -