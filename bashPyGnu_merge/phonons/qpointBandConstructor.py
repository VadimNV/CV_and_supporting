import yaml
import numpy as np

try:
    qptPath=str(raw_input())
except ValueError:
    print "Not a string"
#qptPath='bto/bands_out/noninterpltd/2x2x2_GXMGRM/'

data = yaml.load(open(qptPath+"qpoints.yaml"))
arrayVN = []
A = np.zeros((1,3*data['natom']))  # num of frequencies = num of d.o.f. = numAtm*3 for x,y,z

xaxis=[0.0]
dqm1 = 0.0
dqs = [0.0,0.0,0.0]
for s in range(1,data['nqpoint']): # num of manually specified qpoints (in QPOINTS file and hence in qpoints.yaml)
    q_sm1  = data['phonon'][s-1]['q-position']
    q_s    = data['phonon'][s]['q-position']
    dqs[0] = q_s[0] - q_sm1[0]
    dqs[1] = q_s[1] - q_sm1[1]
    dqs[2] = q_s[2] - q_sm1[2]
    dq     = np.linalg.norm(dqs)
    dqm1  += dq
    xaxis.append(dqm1)

fileGnu=open('qpoint_bands.gnu','w')
for i,qpoint in enumerate(data['phonon']):
    fileGnu.write(str(xaxis[i]))
    for freq in qpoint['band']:
        fr = freq['frequency']
        fileGnu.write('\t'+str(fr))
    fileGnu.write('\n')
fileGnu.close()

# now make gnuplot script to plot all the bands in one go
fGnuPlotter=open('gnuPlotterThisSyst.gnu','w')
fGnuPlotter.write("reset\n")
fGnuPlotter.write("set terminal wxt enhanced font 'Verdana,10' persist\n")
fGnuPlotter.write("unset key\n")
fGnuPlotter.write("set xtics nomirror\n")
fGnuPlotter.write("set ytics nomirror\n")
fGnuPlotter.write("set yrange [-7:30]\n")
fGnuPlotter.write("set arrow from 0.5,-7.0 to 0.5,30.0 nohead lc 'black'\n")
L = len(data['phonon'][0]['band'])
fGnuPlotter.write("plot")
for j in range(0,L-1):
    fGnuPlotter.write(" 'qpoint_bands.gnu' u 1:"+str(j+2)+" w points lc 'blue' pointtype 5 title \"\",\\\n")
fGnuPlotter.write(" 'qpoint_bands.gnu' u 1:"+str(L+1)+" w points lc 'blue' pointtype 5 title \"\"\n")
fGnuPlotter.write("reset\n")
fGnuPlotter.close()
