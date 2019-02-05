# see B. Kanuka's blog: http://bkanuka.com/posts/native-latex-plots/

import matplotlib as mpl
import numpy as np
# import matplotlib.pyplot as plt # B. Kanuka claims this *must* be imported later
# import matplotlib.cm as cm # Later
from mpl_toolkits.basemap import Basemap
import matplotlib.patches as mpatches

mpl.use('pgf')

# ----------------------------------------------------------

# |||\\ difine Python-to-Latex plotting functions //|||
def figsizeTW(scale,TW):
    fig_width_pt = 418.25368                        # README (!): Get this from LaTeX using \the\textwidth
    inches_per_pt = 1.0/72.27                       # Convert pt to inch
    golden_mean = (np.sqrt(5.0)-1.0)/2.0            # Aesthetic ratio (you could change this)
    fig_width = fig_width_pt*inches_per_pt*scale    # width in inches
    if   TW == 'Wide':
        fig_height = fig_width*golden_mean          # height in inches
    elif TW == 'Tall':
        fig_height = fig_width/golden_mean*0.75        # height in inches    
    else             :
        print("VN Error: cannot create figure. Tall or Wide figures only.") # TODO, throw a proper error/exception
    fig_size = [fig_width,fig_height]
    return fig_size

pgf_with_latex = {                       # setup matplotlib to use latex for output
    "legend.numpoints": 1,
    "pgf.texsystem": "pdflatex",         # README (!) change this if using xetex or lautex
    #"pgf.texsystem": "lualatex",         # README (!) change this if using xetex or lautex
    "text.usetex": True,                 # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                    # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    "figure.figsize": figsizeTW(0.9,'Wide'),      # default fig size of 0.9 textwidth
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
#import pylab as pl

# I make my own newfig and savefig functions
def newfigTW(width,TW):
    plt.clf()
    fig = plt.figure(figsize=figsizeTW(width,TW))
    ax  = fig.add_subplot(111)
    return fig, ax

def savefig(filename):
    plt.axis('tight')
    plt.savefig('{}.pgf'.format(filename)) # p**G**f
    plt.savefig('{}.pdf'.format(filename)) # p**D**f

def closefig(fig):
    plt.close(fig)
# ----------------------------------------------------

def setTwoMaps(ax1,ax2):
    m1 = Basemap(projection='eck4',lon_0=0,resolution='c',ax=ax1)
    m1.fillcontinents(color='coral',lake_color='aqua')
    m1.drawparallels(np.arange(-90.,120.,30.))
    m1.drawmeridians(np.arange(0.,360.,60.))
    m1.drawmapboundary(fill_color='aqua')
    m1.drawcoastlines()
    m1.fillcontinents()
    m1.drawmapboundary()
    
    m2 = Basemap(projection='eck4',lon_0=0,resolution='c',ax=ax2)
    m2.fillcontinents(color='coral',lake_color='aqua')
    m2.drawparallels(np.arange(-90.,120.,30.))
    m2.drawmeridians(np.arange(0.,360.,60.))
    m2.drawmapboundary(fill_color='aqua')
    m2.drawcoastlines()
    m2.fillcontinents()
    m2.drawmapboundary()
    return m1, m2
