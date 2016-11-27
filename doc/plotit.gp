CURRENT=0
PREVIOUS=0
FIRST=0

set terminal jpeg
set output 'output.jpg'
plot 'tmp/gasdens'.CURRENT.'.dat' w l title 'curent', \
'tmp/gasdens'.PREVIOUS.'.dat' title 'previous', \
'tmp/gasdens'.FIRST.'.dat'w l ls 2 linecolor rgb 'black' title 'initial'
