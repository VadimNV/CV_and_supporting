reset
set terminal wxt enhanced font 'Verdana,10' persist
unset key
set xtics nomirror
set ytics nomirror
set yrange [-7:30]
plot 'qpoint_bands.gnu' u 1:2 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:3 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:4 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:5 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:6 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:7 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:8 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:9 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:10 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:11 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:12 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:13 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:14 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:15 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:16 w points lc 'blue' pointtype 5 title "",\
 'qpoint_bands.gnu' u 1:17 w points lc 'blue' pointtype 5 title ""
reset
