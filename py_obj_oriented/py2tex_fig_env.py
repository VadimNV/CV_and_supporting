import matplotlib as mpl
#import matplotlib.pyplot as plt # B. Kanuka claims this *must* be imported later
#import matplotlib.cm as cm # Later
#import pylab as pl # Later
import numpy as np

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
    "text.usetex": True,                 # use LaTeX to write all text
    "font.family": "serif",
    "font.serif": [],                    # blank entries should cause plots to inherit fonts from the document
    "font.sans-serif": [],
    "font.monospace": [],
    #"axes.labelsize": 10,               # LaTeX default is 10pt font.
    #"font.size": 10,
    #"legend.fontsize": 8,               # Make the legend/label fonts a little smaller
    #"xtick.labelsize": 8,
    #"ytick.labelsize": 8,
    "figure.figsize": figsize(0.9),      # default fig size of 0.9 textwidth
    "figure.autolayout": True,
    "pgf.preamble": [
        r"\usepackage[utf8x]{inputenc}", # use utf8 fonts becasue your computer can handle it :)
        r"\usepackage[T1]{fontenc}",     # plots will be generated using this preamble
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
    ax = fig.add_subplot(111)
    return fig, ax

def newfigTall(width):
    plt.clf()
    fig = plt.figure(figsize=figsizeTall(width))
    ax = fig.add_subplot(111)
    return fig, ax

def savefig(filename):
    plt.savefig('{}.pgf'.format(filename),bbox_inches = 'tight')
    plt.savefig('{}.pdf'.format(filename),bbox_inches = 'tight')
    #plt.savefig('{}.pgf'.format(filename))
    #plt.savefig('{}.pdf'.format(filename))

def closefig(fig):
    plt.close(fig)

# --------------------- cut -------------------------------
