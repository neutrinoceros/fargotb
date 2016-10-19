#!/bin/bash


#functions and input parameters naming
#--------------------------------------------------

inputfile=$1

function parser { 
cat $1 | grep -i $2 | tr -s ' ' | cut -d ' ' -f 2
}


#parsing
#--------------------------------------------------

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

#conversion into usable variables
oph=$(printf "%.f" $oph)
ninterm=$(printf "%.f" $ninterm)
ntot=$(printf "%.f" $ntot)
seed="${seedjob%.*}"               #seed is now identical to seejob except 
                                   #that it does not contain the extension

#computation
IJON=$((24*$oph))                  #individual job output number, eg number of outputs per job
NJ=$(($ntot/($IJON*$ninterm)))     #number of jobs recquiered by the user


#main loop
#--------------------------------------------------
i=1


#create and edit the new jobs
cd $simdir
while [ $i -le $NJ ]
do
    newfile=$seed\_$i.oar
    restart=$(($IJON*$i))
    cp $seedjob $newfile
    sed -i "s/\$EXECUTABLE/\$EXECUTABLE -s $restart/g" $newfile
    ## DANGER AHEAD
    #//////////////////////////////////////////////////
    if [ $i -eq 1 ] 
    then
        oarsub -S $newfile
    fi

    if [ $i -gt 1 ]
    then
        jobnumber=$(oarstat | grep $USER | tail -1 | cut -d ' ' -f 1) #get the number of the previousjob
        oarsub -S -a $jobnumber $newfile                              #submit the newjob, as an appendage of the previous one
    fi
    #END OF DANGER ZONE
    #\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    i=$(($i+1))
done
cd -