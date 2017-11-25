# http://gnuplot-tricks.blogspot.co.uk/2010/06/broken-axis-once-more.html
reset
set terminal wxt enhanced font 'Verdana,10' persist
unset key
bm = 0.15
lm = 0.12
rm = 0.95
gap = 0.03
size = 0.75
y1 = 1.55; y2 = 1.6; y3 = 2.275; y4 = 2.325

set multiplot
set key at 20,1.64
set xlabel 'Ion #'
set border 1+2+8
set xtics nomirror
set ytics nomirror
set lmargin at screen lm
set rmargin at screen rm
set bmargin at screen bm
set tmargin at screen bm + size * (abs(y2-y1) / (abs(y2-y1) + abs(y4-y3) ) )

set yrange [y1:y2]
plot [0:24] '../TiO2_rut2x2x3_300K_St1_50Ry_Lowdin-s-p-d-Z.dat' every ::0::23 u 9 w points pointtype 5 title "",\
'../TiO2_rut2x2x3_300K_St1_50Ry_Lowdin-s-p-d-Z.dat' every ::0::23 u 9 w l lc 'blue' title "DFT Lowdin"

# ----

set key at 20,2.32
unset xtics
unset xlabel
set border 2+4+8
set bmargin at screen bm + size * (abs(y2-y1) / (abs(y2-y1) + abs(y4-y3) ) ) + gap
set tmargin at screen bm + size + gap
set yrange [y3:y4]

set label 'Lowdin ionic charge [e]' at screen 0.03, bm + 0.5 * (size + gap) offset 0,-strlen("Lowdin ionic charge [e]")/4.0 rotate by 90

set arrow from screen lm - gap / 4.0, bm + size * (abs(y2-y1) / (abs(y2-y1)+abs(y4-y3) ) ) - gap / 4.0 to screen \
lm + gap / 4.0, bm + size * (abs(y2-y1) / (abs(y2-y1) + abs(y4-y3) ) ) + gap / 4.0 nohead

set arrow from screen lm - gap / 4.0, bm + size * (abs(y2-y1) / (abs(y2-y1)+abs(y4-y3) ) ) - gap / 4.0  + gap to screen \
lm + gap / 4.0, bm + size * (abs(y2-y1) / (abs(y2-y1) + abs(y4-y3) ) ) + gap / 4.0 + gap nohead

set arrow from screen rm - gap / 4.0, bm + size * (abs(y2-y1) / (abs(y2-y1)+abs(y4-y3) ) ) - gap / 4.0 to screen \
rm + gap / 4.0, bm + size * (abs(y2-y1) / (abs(y2-y1) + abs(y4-y3) ) ) + gap / 4.0 nohead

set arrow from screen rm - gap / 4.0, bm + size * (abs(y2-y1) / (abs(y2-y1)+abs(y4-y3) ) ) - gap / 4.0  + gap to screen \
rm + gap / 4.0, bm + size * (abs(y2-y1) / (abs(y2-y1) + abs(y4-y3) ) ) + gap / 4.0 + gap nohead

plot [0:24] '../asapTiO2_rut2x2x3_300K_St1_ForGNUPLOT-final.dat' every ::0::23 u 5 w points pointtype 5 title "",\
'../asapTiO2_rut2x2x3_300K_St1_ForGNUPLOT-final.dat' every ::0::23 u 5 w l lt '-' lw 2 lc 'blue' title "ASAP q_i/{/Symbol \326}{/Symbol e}"

unset multiplot
