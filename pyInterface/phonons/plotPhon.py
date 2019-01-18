import yaml
import numpy as np

figPath          = 'bto/figsPhon/'
figName          = 'QEqTi6x6x6s1_2_3_4_5_100K_interpolated'
interPolatedFile = 'all_workDir/workDir_QEqTS6x6x6_100K_s1_2_4_5out/interpolated/band.yaml'
#interPolatedFile = 'all_workDir/workDir_QEqTS6x6x6_100K_s1_2_4_5out/interpolated_nac/band.yaml'
exactFile_sc1    = 'all_workDir/workDir_QEqTS6x6x6_100K_s1_2_4_5out/qpoint_bands.gnu'
exactFile0Kn6    = '../phonons/bto/bands_out/noninterpltd/QEqTi/6x6x6_GXMGRM/qpoint_bands.gnu'
exactFile0Kn7    = '../phonons/bto/bands_out/noninterpltd/QEqTi/7x7x7_GXMGRM/qpoint_bands.gnu'
exactFile0Kn8    = '../phonons/bto/bands_out/noninterpltd/QEqTi/8x8x8_GXMGRM/qpoint_bands.gnu'
exactFile0Kn9    = '../phonons/bto/bands_out/noninterpltd/QEqTi/9x9x9_GXMGRM/qpoint_bands.gnu'
exactFile0Kn10   = '../phonons/bto/bands_out/noninterpltd/QEqTi/10x10x10_GXMGRM/qpoint_bands.gnu'

# _| interpolated
with open(interPolatedFile, 'r') as interPolatedIO:
    try:
        interPolatedYAML = yaml.safe_load(interPolatedIO)
    except yaml.YAMLError as exc:
        print(exc)
qLast   = [0.0,0.0,0.0]
dqTot   = 0.0
dqQpath = []
qQpath  = []
frQpath = []
for i,qpoint in enumerate(interPolatedYAML['phonon']):
    qPos  = qpoint['q-position']
    dq    = np.linalg.norm([ q-q0 for (q,q0) in zip(qPos,qLast) ])
    dqTot += dq
    frThis = []
    for freq in qpoint['band']:
        fr = freq['frequency']
        frThis.append(fr)
    frQpath.append( frThis )
    dqQpath.append( dqTot  )
    qQpath.append(  qPos   )
    qLast = [qx for qx in qPos]

# _| exact
dqQpath_Exct = []
frQpath_Exct = []
with open(exactFile_sc1) as exactIO:
    content = exactIO.readlines()
    content = [x.strip() for x in content]
    for line in content:
        dqQpath_Exct.append(              float(line.split()[0])  )
        frQpath_Exct.append( [float(f) for f in line.split()[1:]] )
# _| exact T=0K 6x6x6
dqQpath_Exct0Kn6 = []
frQpath_Exct0Kn6 = []
with open(exactFile0Kn6) as exactIO:
    content = exactIO.readlines()
    content = [x.strip() for x in content]
    for line in content:
        dqQpath_Exct0Kn6.append(              float(line.split()[0])  )
        frQpath_Exct0Kn6.append( [float(f) for f in line.split()[1:]] )
# _| exact T=0K 7x7x7
dqQpath_Exct0Kn7 = []
frQpath_Exct0Kn7 = []
with open(exactFile0Kn7) as exactIO:
    content = exactIO.readlines()
    content = [x.strip() for x in content]
    for line in content:
        dqQpath_Exct0Kn7.append(              float(line.split()[0])  )
        frQpath_Exct0Kn7.append( [float(f) for f in line.split()[1:]] )
# _| exact T=0K 8x8x8
dqQpath_Exct0Kn8 = []
frQpath_Exct0Kn8 = []
with open(exactFile0Kn8) as exactIO:
    content = exactIO.readlines()
    content = [x.strip() for x in content]
    for line in content:
        dqQpath_Exct0Kn8.append(              float(line.split()[0])  )
        frQpath_Exct0Kn8.append( [float(f) for f in line.split()[1:]] )
# _| exact T=0K 9x9x9
dqQpath_Exct0Kn9 = []
frQpath_Exct0Kn9 = []
with open(exactFile0Kn9) as exactIO:
    content = exactIO.readlines()
    content = [x.strip() for x in content]
    for line in content:
        dqQpath_Exct0Kn9.append(              float(line.split()[0])  )
        frQpath_Exct0Kn9.append( [float(f) for f in line.split()[1:]] )
# _| exact T=0K 10x10x10
dqQpath_Exct0Kn10 = []
frQpath_Exct0Kn10 = []
with open(exactFile0Kn10) as exactIO:
    content = exactIO.readlines()
    content = [x.strip() for x in content]
    for line in content:
        dqQpath_Exct0Kn10.append(              float(line.split()[0])  )
        frQpath_Exct0Kn10.append( [float(f) for f in line.split()[1:]] )

# ...set up matplotlib stuff
import matplotlib as mpl
import matplotlib.patches as mpatches
mpl.use('pgf')

# --------------------------- cut -------------------------------

# |||\\ difine Python-to-Latex plotting functions //|||
def figsize(scale):
    fig_width_pt = 418.25368 # 469.755              # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    fig_height = fig_width*golden_mean              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

def figsizeTall(scale):
    fig_width_pt = 418.25368 # 469.755              # Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    fig_height = fig_width/golden_mean*0.75              # height in inches
    fig_size = [fig_width,fig_height]
    return fig_size

pgf_with_latex = {                       # setup matplotlib to use latex for output
    "pgf.texsystem": "pdflatex",         # change this if using xetex or lautex
    #"pgf.texsystem": "lualatex",         # change this if using xetex or lautex
    "text.usetex": True,                 # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                    # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "figure.figsize": figsize(0.9),      # default fig size of 0.9 textwidth
    "figure.autolayout": True,
    "pgf.rcfonts":False,
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}", # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",     # plots will be generated using this preamble
        r"\usepackage{amsmath}",
        ]
    }
mpl.rcParams.update(pgf_with_latex)
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pylab as pl
# I make my own newfig and savefig functions
def newfig(width):
    plt.clf()
    fig = plt.figure(figsize=figsize(width))
    ax  = fig.add_subplot(111)
    return fig, ax
def newfigTall(width):
    plt.clf()
    fig = plt.figure(figsize=figsizeTall(width))
    ax = fig.add_subplot(111)
    return fig, ax
def savefigNonTight(filename):
    plt.savefig('{}.pgf'.format(filename)) # p**G**f
    plt.savefig('{}.pdf'.format(filename)) # p**D**f
def savefig(filename):
    plt.axis('tight')
    plt.savefig('{}.pgf'.format(filename)) # p**G**f
    plt.savefig('{}.pdf'.format(filename)) # p**D**f
def closefig(fig):
    plt.close(fig)
#____________________________________________________________________

xAll       = [ dqT      for dqT   in dqQpath       ]
xAll_Exct  = [ dqT      for dqT   in dqQpath_Exct  ]
xAll_Exct0Kn6= [ dqT      for dqT   in dqQpath_Exct0Kn6 ]
xAll_Exct0Kn7= [ dqT      for dqT   in dqQpath_Exct0Kn7 ]
xAll_Exct0Kn8= [ dqT      for dqT   in dqQpath_Exct0Kn8 ]
xAll_Exct0Kn9= [ dqT      for dqT   in dqQpath_Exct0Kn9 ]
xAll_Exct0Kn10= [ dqT      for dqT   in dqQpath_Exct0Kn10 ]
figTk      = plt.figure(figsize=figsize(0.9) )

patch_set  = []

#for j in range(len(frQpath[0])):
#    y_j         = [ frSet[j] for frSet in frQpath ]
#    #this_patch, = plt.plot( xAll[17:]  , y_j[17:], marker='None', linestyle='-'   , label=r'$\delta $'   , color='blue' )
#    this_patch, = plt.plot( xAll[  :]  , y_j[  :] , marker='None', linestyle='-'   , label=r'$\delta $'   , color='blue' )
for j in range(len(frQpath_Exct0Kn7[0])):
    y_j         = [ frSet[j] for frSet in frQpath_Exct0Kn6 ]
    this_patch, = plt.plot( xAll_Exct0Kn6 , y_j      , marker='.' , linestyle='None', label=r'$\delta $'   , color='blue' )
    y_j         = [ frSet[j] for frSet in frQpath_Exct0Kn7 ]
    this_patch, = plt.plot( xAll_Exct0Kn7 , y_j      , marker='.' , linestyle='None', label=r'$\delta $'   , color='blue' )
    y_j         = [ frSet[j] for frSet in frQpath_Exct0Kn8 ]
    this_patch, = plt.plot( xAll_Exct0Kn8 , y_j      , marker='.' , linestyle='None', label=r'$\delta $'   , color='blue' )
    y_j         = [ frSet[j] for frSet in frQpath_Exct0Kn9 ]
    this_patch, = plt.plot( xAll_Exct0Kn9 , y_j      , marker='.' , linestyle='None', label=r'$\delta $'   , color='blue' )
    y_j         = [ frSet[j] for frSet in frQpath_Exct0Kn10 ]
    this_patch, = plt.plot( xAll_Exct0Kn10, y_j      , marker='.' , linestyle='None', label=r'$\delta $'   , color='blue' )
for j in range(len(frQpath_Exct[0])):
    y_j         = [ frSet[j] for frSet in frQpath_Exct ]
    this_patch, = plt.plot( xAll_Exct     , y_j      , marker='.' , linestyle='None', label=r'$\delta $'   , color='green' )


#plt.legend(handles=patch_set,bbox_to_anchor=(0.11, 0.42),loc=8, borderaxespad=0.,fontsize=8)
plt.ylim([-5,25])
plt.xlim([0.0,3.1])
plt.savefig('{}.pgf'.format(figPath+'/'+figName),bbox_inches='tight') # p**G**f
plt.savefig('{}.pdf'.format(figPath+'/'+figName),bbox_inches='tight') # p**D**f
closefig(figTk)
