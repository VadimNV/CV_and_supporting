# http://gnuplot-tricks.blogspot.co.uk/2010/06/broken-axis-once-more.html
reset
set terminal wxt enhanced font 'Verdana,10' persist
unset key

set key at 20,1.64
set xlabel 'Ion #'

set xtics nomirror
set ytics nomirror
# set lmargin at screen lm
# set rmargin at screen rm
# set bmargin at screen bm
# set tmargin at screen bm + size * (abs(y2-y1) / (abs(y2-y1) + abs(y4-y3) ) )

set yrange [y1:y2]
plot [-0.2:1.2] '../BurgerPathASAP.txt' u 1:7 w points pointtype 5 title "",\
'../BurgerPathASAP.txt' u 1:7 w l lc 'blue' title "DFT Lowdin"


# set label 'Lowdin ionic charge [e]' at screen 0.03, bm + 0.5 * (size + gap) offset 0,-strlen("Lowdin ionic charge [e]")/4.0 rotate by 90
