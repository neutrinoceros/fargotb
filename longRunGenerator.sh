#!/bin/bash

inputfile=$1

function parser { 
cat $1 | grep -i $2 | tr -s ' ' | cut -d ' ' -f 2
}

#read the input file displaying all necessary information

simdir=$(parser $inputfile simdir)
configdir=$simdir/$(parser $inputfile configdir)
jobsdir=$simdir/$(parser $inputfile jobsdir)
seedjob=$jobsdir/$(parser $inputfile seedjob)
configfile=$configdir/$(parser $inputfile configfile)
oph=$(parser $inputfile oph)

#go into the configuration file to grasp more details
ninterm=$(parser $configfile ninterm)
ntot=$(parser $configfile ntot)

#conversion into proper numbers
oph=$(printf "%.f" $oph)
ninterm=$(printf "%.f" $ninterm)
ntot=$(printf "%.f" $ntot)


#computation
IJON=$((24*$oph))                  #individual job output number, eg number of outputs per job
NJ=$(($ntot/($IJON*$ninterm)))     #number of jobs recquiered by the user


i=1
seed="${seedjob%.*}" #seed is now identical to seejob except that it does not contain the extension


#create and edit the new jobs
cd $simdir
while [ $i -le $NJ ]
do
    newfile=$seed\_$i.oar
    restart=$(($IJON*$i))
    cp $seedjob $newfile
    sed -i "s/\$EXECUTABLE/\$EXECUTABLE -s $restart/g" $newfile
    ## DANGER AHEAD
    if [ $i -eq 1 ] 
    then
        oarsub -S $newfile
    fi

    if [ $i -gt 1 ]
    then
        jobnumber=$(oarstat | grep crobert | tail -1 | cut -d ' ' -f 1)
        oarsub -S -a $jobnumber $newfile
    fi
    #END OF DANGER ZONE
    i=$(($i+1))
done
cd -