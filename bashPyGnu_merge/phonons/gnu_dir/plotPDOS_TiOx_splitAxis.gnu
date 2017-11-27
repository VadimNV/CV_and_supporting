set output "TiO2rut2x2x3_300K_St1_pdos_orbitalSplit.ps"

reset
set terminal wxt enhanced font 'Verdana,10' persist
unset key
bm = 0.15
lm = 0.12
# rm = 0.95
tm = 0.95
gap = 0.015
size = 0.75
x0a = -34.3; x0b = -32.3 ; x1 = -19.2; x2 = -15.8; x3 = -6.8; x4 = 0.0
r = (abs(x2-x1)/(abs(x2-x1)+abs(x4-x3)))
delTic = 5.0

set multiplot

set ylabel 'DOS'
set border 1+2+4 # bottom+left+top
set xtics nomirror x0a+0.3, 1.0  , x0b - 0.1
set ytics nomirror
set lmargin at screen lm
set rmargin at screen lm + size * (abs(x0b-x0a) / (abs(x0b-x0a) + abs(x2-x1) + abs(x4-x3) ) )
set bmargin at screen bm
set tmargin at screen tm

set yrange [0:105]
set xrange [x0a:x0b]
plot '../TiO2_rut2x2x3_300K_St1.pdos_tot' u ($1-9.3):2 w l lw 2 linecolor "black",\
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#1to24(Ti)_wfc#2(p)' u ($1-9.3):3 w l lw 2 , \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#1to24(Ti)_wfc#3(s)' u ($1-9.3):3 w l lw 2 , \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#1to24(Ti)_wfc#4(d)' u ($1-9.3):3 w l lw 2 , \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#25to72(O)_wfc#1(s)' u ($1-9.3):3 w l lt '-' lw 2 lc "purple" , \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#25to72(O)_wfc#2(p)' u ($1-9.3):3 w l lt '-' lw 2 lc "red"

# ----
unset ylabel
set border 1+4 # bottom+top
set xtics nomirror x1+0.2, 1.0  , x2 - 0.1
unset ytics
set lmargin at screen lm + size * (abs(x0b-x0a) / (abs(x0b-x0a) + abs(x2-x1) + abs(x4-x3) ) ) + gap
set rmargin at screen lm + size * ((abs(x2-x1) + abs(x0b-x0a)) / (abs(x0b-x0a) + abs(x2-x1) + abs(x4-x3) ) )
set bmargin at screen bm
set tmargin at screen tm

set yrange [0:105]
set xrange [x1:x2]
plot '../TiO2_rut2x2x3_300K_St1.pdos_tot' u ($1-9.3):2 w l lw 2 linecolor "black",\
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#1to24(Ti)_wfc#2(p)' u ($1-9.3):3 w l lw 2 , \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#1to24(Ti)_wfc#3(s)' u ($1-9.3):3 w l lw 2 , \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#1to24(Ti)_wfc#4(d)' u ($1-9.3):3 w l lw 2 , \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#25to72(O)_wfc#1(s)' u ($1-9.3):3 w l lt '-' lw 2 lc "purple" , \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#25to72(O)_wfc#2(p)' u ($1-9.3):3 w l lt '-' lw 2 lc "red" 

# ----

set xtics nomirror x3+0.8, 1.0  , x4
unset ytics
unset ylabel
set border 1+4+8 # bottom+top+right
set rmargin at screen lm + size + gap
set lmargin at screen lm + size * ((abs(x2-x1) + abs(x0b-x0a)) / (abs(x0b-x0a) + abs(x2-x1) + abs(x4-x3) ) ) + gap
set yrange [0:105]
set xrange [x3:x4]

set label 'Energy[eV]' at screen lm + 0.4 * size , bm * 0.35 ,-strlen("Energy[eV]")/4.0 

set arrow from screen lm + size * (abs(x0b-x0a) / (abs(x0b-x0a)+abs(x2-x1)+abs(x4-x3) ) ) - gap / 4.0 , bm - gap to screen \
lm + size * (abs(x0b-x0a) / (abs(x0b-x0a) + abs(x2-x1) + abs(x4-x3) ) ) + gap / 4.0 , bm + gap nohead

set arrow from screen lm + size * (abs(x0b-x0a) / (abs(x0b-x0a)+abs(x2-x1)+abs(x4-x3) ) ) - gap / 4.0 + gap , bm - gap to screen \
lm + size * (abs(x0b-x0a) / (abs(x0b-x0a)+abs(x2-x1) + abs(x4-x3) ) ) + gap / 4.0 + gap, bm + gap nohead
 
set arrow from screen lm + size * (abs(x0b-x0a) / (abs(x0b-x0a)+abs(x2-x1)+abs(x4-x3) ) ) - gap / 4.0 , tm - gap to screen \
lm + size * (abs(x0b-x0a) / (abs(x0b-x0a)+abs(x2-x1) + abs(x4-x3) ) ) + gap / 4.0 , tm + gap nohead

set arrow from screen lm + size * (abs(x0b-x0a) / (abs(x0b-x0a)+abs(x2-x1)+abs(x4-x3) ) ) - gap / 4.0 + gap , tm - gap to screen \
lm + size * (abs(x0b-x0a) / (abs(x0b-x0a)+abs(x2-x1) + abs(x4-x3) ) ) + gap / 4.0 + gap, tm + gap nohead

# --

set arrow from screen lm + size * ((abs(x2-x1)+abs(x0b-x0a)) / (abs(x0b-x0a)+abs(x2-x1)+abs(x4-x3) ) ) - gap / 4.0 , bm - gap to screen \
lm + size * ((abs(x2-x1)+abs(x0b-x0a)) / (abs(x0b-x0a) + abs(x2-x1) + abs(x4-x3) ) ) + gap / 4.0 , bm + gap nohead

set arrow from screen lm + size * ((abs(x2-x1)+abs(x0b-x0a)) / (abs(x0b-x0a)+abs(x2-x1)+abs(x4-x3) ) ) - gap / 4.0 + gap , bm - gap to screen \
lm + size * ((abs(x2-x1)+abs(x0b-x0a)) / (abs(x0b-x0a)+abs(x2-x1) + abs(x4-x3) ) ) + gap / 4.0 + gap, bm + gap nohead
 
set arrow from screen lm + size * ((abs(x2-x1)+abs(x0b-x0a)) / (abs(x0b-x0a)+abs(x2-x1)+abs(x4-x3) ) ) - gap / 4.0 , tm - gap to screen \
lm + size * ((abs(x2-x1)+abs(x0b-x0a)) / (abs(x0b-x0a)+abs(x2-x1) + abs(x4-x3) ) ) + gap / 4.0 , tm + gap nohead

set arrow from screen lm + size * ((abs(x2-x1)+abs(x0b-x0a)) / (abs(x0b-x0a)+abs(x2-x1)+abs(x4-x3) ) ) - gap / 4.0 + gap , tm - gap to screen \
lm + size * ((abs(x2-x1)+abs(x0b-x0a)) / (abs(x0b-x0a)+abs(x2-x1) + abs(x4-x3) ) ) + gap / 4.0 + gap, tm + gap nohead

set key at -1.0,104
plot '../TiO2_rut2x2x3_300K_St1.pdos_tot' u ($1-9.3):2 w l lw 2 linecolor "black" title "DOS",\
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#1to24(Ti)_wfc#2(p)' u ($1-9.3):3 w l lw 2 title "Ti 3p pDOS", \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#1to24(Ti)_wfc#3(s)' u ($1-9.3):3 w l lw 2 title "Ti 4s pDOS", \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#1to24(Ti)_wfc#4(d)' u ($1-9.3):3 w l lw 2 title "Ti 3d pDOS", \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#25to72(O)_wfc#1(s)' u ($1-9.3):3 w l lt '-' lw 2 lc "purple" title "O 2s pDOS", \
'../pdos_dir/TiO2_rut2x2x3_300K_St1.pdos_atm#25to72(O)_wfc#2(p)' u ($1-9.3):3 w l lt '-' lw 2 lc "red" title "O 2p pDOS"

unset multiplot
