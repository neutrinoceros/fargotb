#!/bin/bash

# init
#-------------------------------------------------------------

cat doc/plotit.gp > plotit.gp
gnuplot plotit.gp
eog output.jpg &


# watching
#-------------------------------------------------------------

previous="0"
previous_num=0
old="-1"
continue=true
while [[ $continue == true ]]
do
    #exctration is a unecessarily complicated
    new=$(ls -ltr tmp/ | grep gasdens | tail --lines 1 \
                 | tr -s ' ' | cut -d ' ' -f 9 \
                 | sed 's![a-z]!!g' | cut -d . -f 1)
    new_num=$(printf "%.f" $new)
    if (( $new_num > $previous_num ))
    then
        echo "refresh, now at $new"
        sed -i "s?CURRENT=$previous?CURRENT=$new?g" plotit.gp
        sed -i "s?PREVIOUS=$old?PREVIOUS=$previous?g" plotit.gp
        gnuplot plotit.gp
        old=$previous
        previous=$new
        previous_num=$(printf "%.f" $new)
    fi
    sleep 1
done
