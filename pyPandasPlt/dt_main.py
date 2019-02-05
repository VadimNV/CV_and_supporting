# Vadim Nemytov.
# tested using Python 2.7
# README (!): if you want to run this code, make sure latex file "story/story_temp.tex" has the correct absolute path to your working directory. (this is to input pgf's)
# README (!): see setup_mpl.py for "pdflatex" vs "lualatex" and other system-dependent LaTeX parameters.
# README (!): the code and comments have been optimised for viewing on a fairly large, BenQ GL2450 - 24", monitor. Apologies if lines start folding back on your screen.

import numpy as np
import pandas as pd
import itertools
import math
import os
import subprocess
from setup_mpl import * # mpl setup to export figs in .pgf for a seemless integration with LaTeX; also .pdf
from setup_tex import * # create .tex document that compiles to give a simple PDF presentation

dtPath  = "dataDir/"
figPath = "story/figs/"
texPath = "story/"
fAE     = dtPath + "athlete_events.csv"
fNOC    = dtPath + "noc_regions.csv"
dfAE    = pd.read_csv(fAE)
dfNOC   = pd.read_csv(fNOC)

nanTol  = 0.90 # if num of NaN is less than nanTol of total entries, then the data for that year/sport is good

# ~ Part I   ~ Prepare the data, deal with the missing values
# TODO ...for the sake of this exercise, not dealing with missing values. I am interested in mean values by year, but these are reliable only for 1950's onward --> the plots would be too "short" and boring (but more realiable).

# ~ Part II  ~ Make some figures

# ___| 1 |___ Height and Weight by sport - scatter plot
figName_WHscatter = 'HW_scatter'
fig, ax           = newfigTW(0.9,'Wide')
plt.arrow(78.9,168,-30,   0,linestyle='-',color='slategrey',head_width=0.7,zorder=1,length_includes_head=True)
plt.arrow(78.9,168,  0,18.7,linestyle='-',color='slategrey',head_width=0.7,zorder=1,length_includes_head=True)
plt.text(78.9-15,168-2, r'$\sim30$ kg', fontsize=9)
plt.text(78.9+1 ,168+8, r'$\sim20$ cm', fontsize=9)
dfAE[['Sport','Height','Weight'] ].reset_index().groupby('Sport').mean().plot(x='Weight',y='Height',kind='scatter', color='slateblue',ax=ax,zorder=2)           # mean values grouped by sport -> scatter plot
shortest = dfAE[['Sport','Height','Weight'] ].reset_index().groupby('Sport').mean().sort_values(by=['Height']                ).reset_index().iloc[0,:].tolist() # smallest mean height, grouped by sport
tallest1 = dfAE[['Sport','Height','Weight'] ].reset_index().groupby('Sport').mean().sort_values(by=['Height'],ascending=False).reset_index().iloc[0,:].tolist()
tallest2 = dfAE[['Sport','Height','Weight'] ].reset_index().groupby('Sport').mean().sort_values(by=['Height'],ascending=False).reset_index().iloc[1,:].tolist()
heaviest = dfAE[['Sport','Height','Weight'] ].reset_index().groupby('Sport').mean().sort_values(by=['Weight'],ascending=False).reset_index().iloc[0,:].tolist()
lightest = dfAE[['Sport','Height','Weight'] ].reset_index().groupby('Sport').mean().sort_values(by=['Weight']                ).reset_index().iloc[0,:].tolist()
dfN      = dfAE[['Sport','Height','Weight'] ].reset_index().groupby('Sport').mean().reset_index()                                                               # conditionally, find mean values close to 79kg,169cm
middle   = dfN.loc[ (np.abs(dfN['Weight']-79)<2) & (np.abs(dfN['Height']-168)<2) ].iloc[0,:].tolist()                                                           #
nicePts  = [shortest, lightest, middle, tallest2, tallest1, heaviest]
shifts   = [  [1,-1],  [-8,-2], [1,-1],    [0,1],    [1,1],   [-6,1]]
for pt, shift in zip(nicePts,shifts):
    plt.text(pt[-1]+shift[0], pt[-2]+shift[1], pt[0], fontsize=9)                                                                                               # place text near these points of interest (shortest, etc.)
#
plt.savefig('{}.pgf'.format(figPath+figName_WHscatter),bbox_inches='tight') # p**G**f
plt.savefig('{}.pdf'.format(figPath+figName_WHscatter),bbox_inches='tight') # p**D**f
plt.close(fig)
#____________

# ___| 2 |___ Height and Weight in Gymnastics over the years - line plot + linear fit
figName_WHgymnstcsByYear          = 'GymnasticsYearly'
fig, (ax1, ax2)                   = plt.subplots(2, sharex=True, sharey=False,figsize=figsizeTW(0.9,'Wide'))
mpl.rcParams['figure.autolayout'] = False
fig, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False,figsize=figsizeTW(0.9,'Wide'))
# ...Height
dfAE.loc[ dfAE['Sport']=='Gymnastics'                               , ['Year','Height','Weight' ]].reset_index().groupby('Year').mean().plot(y='Height',ax=ax1, marker='.',linestyle='', color='black', legend=False)
dfAE.loc[(dfAE['Sport']=='Gymnastics') & (dfAE['Medal']=='Gold')    , ['Year','Height','Weight' ]].reset_index().groupby('Year').mean().plot(y='Height',ax=ax1, marker='.',linestyle='', color='orange',legend=False)
x               = dfAE.loc[(dfAE['Sport']=='Gymnastics') & np.isfinite(dfAE['Weight']), ['Year','Height'          ]].reset_index().groupby('Year').mean().iloc[:,1].index.tolist() # "x", a list of years
y               = dfAE.loc[(dfAE['Sport']=='Gymnastics') & np.isfinite(dfAE['Weight']), ['Year','Height'          ]].reset_index().groupby('Year').mean().iloc[:,1].tolist()       # "y", a list of Heights
fit             = np.polyfit(x,y,1)                                                                                                                                                # order-1 poly, i.e. y=m*x+b (linear fit)
fit_fn          = np.poly1d(fit)
ax1.plot(x, fit_fn(x), '--k')
# ...Weight
dfAE.loc[ dfAE['Sport']=='Gymnastics'                               , ['Year','Height','Weight' ]].reset_index().groupby('Year').mean().plot(y='Weight',ax=ax2, marker='.',linestyle='',color='black', legend=False)
dfAE.loc[(dfAE['Sport']=='Gymnastics') & (dfAE['Medal']=='Gold')    , ['Year','Height','Weight' ]].reset_index().groupby('Year').mean().plot(y='Weight',ax=ax2, marker='.',linestyle='',color='orange',legend=False)
x               = dfAE.loc[(dfAE['Sport']=='Gymnastics') & np.isfinite(dfAE['Weight']), ['Year','Weight'          ]].reset_index().groupby('Year').mean().iloc[:,1].index.tolist() # "x", a list of years
y               = dfAE.loc[(dfAE['Sport']=='Gymnastics') & np.isfinite(dfAE['Weight']), ['Year','Weight'          ]].reset_index().groupby('Year').mean().iloc[:,1].tolist()       # "y", a list of Weights
fit             = np.polyfit(x,y,1)                                                                                                                                                # order-1 poly, i.e. y=m*x+b (linear fit)
fit_fn          = np.poly1d(fit)
# ...
ax2.plot(x, fit_fn(x), '--k')
ax1.set_ylim(   [156.5,177.5] )
ax2.set_ylim(   [ 47.5, 77.5] )
ax2.set_xlim(   [ 1893, 2020] )
ax1.set_ylabel( 'Height [cm]' )
ax2.set_ylabel( 'Weight [kg]' )
ax2.get_yaxis().set_label_coords(-0.09,0.5)
fig.subplots_adjust(hspace=0)
plt.savefig('{}.pgf'.format(figPath+figName_WHgymnstcsByYear),bbox_inches='tight') # p**G**f
plt.savefig('{}.pdf'.format(figPath+figName_WHgymnstcsByYear),bbox_inches='tight') # p**D**f
plt.close(fig)
mpl.rcParams['figure.autolayout'] = True
# TODO see if Basketball players' height histogram shows several peaks, i.e. players specialise within the team into short-range and long-range shooters.
#____________

# ___| 3 |___ Winter/Summer winners per country. The influence of climate. Download coordinates of the countries.
figName_Maps        = 'mapsSeason'
fileLatLong         = r'country_centroids.csv'            # file with country centroids (their mean latitude and longitude)
if os.path.isfile(dtPath+fileLatLong) :                   # see if the file is already downloaded
    dfLatLong         = pd.read_csv(dtPath+fileLatLong)
else                                  :                   # else - download it
    # |
    #  http://worldmap.harvard.edu/download/wfs/34645/csv?outputFormat=csv&amp;service=WFS&amp;request=GetFeature&amp;format_options=charset%3AUTF-8&amp;typename=geonode%3Acountry_centroids_az8&amp;version=1.0.0
    #  OR manually: visit https://worldmap.harvard.edu/data/geonode:country_centroids_az8 and click "CSV"
    # |
    cntryLatLongURL = r'http://worldmap.harvard.edu/download/wfs/34645/csv?outputFormat=csv&amp;service=WFS&amp;request=GetFeature&amp;format_options=charset%3AUTF-8&amp;typename=geonode%3Acountry_centroids_az8&amp;version=1.0.0'
    os.chdir(dtPath)
    devnull         = open(os.devnull, 'w')
    myCommand       = ' wget -O '+fileLatLong+' '+cntryLatLongURL
    print myCommand.split()
    subprocess.call(myCommand.split()) #,stdout=devnull,stderr=devnull)
    os.chdir('../')  
    dfLatLong       = pd.read_csv(dtPath+fileLatLong)
#
dfLatLong           = dfLatLong.loc[:,['admin','Longitude','Latitude']]
dfLatLong.rename(columns = {'admin':'region'}, inplace = True)
dfLatLong.loc[ dfLatLong['region']=='United Kingdom'          ,['region']] ='UK'                                                           # The downloaded file and the Olympics dataset, 
dfLatLong.loc[ dfLatLong['region']=='United States of America',['region']] ='USA'                                                          # ...use different conventions for a few countries, e.g. UK and USA
#
dfNew               = pd.merge(dfAE,dfNOC.loc[:,['NOC','region']], on='NOC',how='outer')                                                   # link dfAE to dfNOC, to get countries' names.
dfNew2              = pd.merge(dfNew,dfLatLong.loc[:,['region','Latitude','Longitude']], on='region',how='outer')                          # then link countries' names to centroids (location on the map) from the downloaded CSV file.
pv                  = pd.pivot_table(dfNew2, values='Medal', index=['region','Latitude','Longitude'], columns=['Season'], aggfunc='count') # Count Gold medals per country, per season
pv                  = pv.fillna(0)
pv                  = pv.reset_index()
totS, totW          = pv['Summer'].sum() , pv['Winter'].sum()
pv.loc[:,'Summer'] *= (1.0/totS)                                                                                                           # normalise number of Gold medal w.r.t. to total ever won.
pv.loc[:,'Winter'] *= (1.0/totW)
#
fig, (ax1, ax2)     = plt.subplots(2, 1,figsize=figsizeTW(1.1,'Wide'))
m1, m2              = setTwoMaps(ax1,ax2)
MRK                 = 100
for i, (index, row) in enumerate(pv.iterrows()):
    Lat, Long       = row['Latitude'], row['Longitude']
    x, y            = m1(Long, Lat)
    Ms,Mw           = row['Summer']*MRK, row['Winter']*MRK
    if Ms > 0:
        if Ms<2: Ms = 2
        ax1.plot(x, y, 'o',color='palevioletred', markersize=Ms)                                                                           # the size of the bubble/disk/point is proportional to the normalised medal count.
    if Mw > 0:
        if Mw<2: Mw = 2
        ax2.plot(x, y, 'o',color='slateblue', markersize=Mw)
p_set1, p_set2      = [] , []
for pc,st in zip([15,10,5,2],['15','10','5','<2']):                                                                                        # at legend to give a sense of how the bubble size relates to normalised medal count
    this_patch,     = ax1.plot([], [], 'o',color='palevioletred', markersize=pc, label=r'$'+st+r'\%$')
    p_set1.append(this_patch)
    this_patch,     = ax2.plot([], [], 'o',color='slateblue', markersize=pc, label=r'$'+st+r'\%$')
    p_set2.append(this_patch)
ax1.legend(handles=p_set1)
ax1.legend(fontsize=8,loc='lower left', bbox_to_anchor=(-0.08, 0.), borderaxespad=0.,borderpad=0.75, labelspacing=0.9)
ax2.legend(handles=p_set2)
ax2.legend(fontsize=8,loc='lower left', bbox_to_anchor=(-0.08, 0.), borderaxespad=0.,borderpad=0.75, labelspacing=0.9)
plt.savefig('{}.pgf'.format(figPath+figName_Maps),bbox_inches='tight') # p**G**f
plt.savefig('{}.pdf'.format(figPath+figName_Maps),bbox_inches='tight') # p**D**f
plt.close(fig)
#____________


# ~ Part III ~ Embed in LaTeX
fTemp = texPath+'story_template.tex' # template
fOut  = texPath+'story.tex'          # final result, in landscape, pdf

with open(fTemp) as ioTemp, open(fOut,'w') as ioOut:
    content = ioTemp.readlines()
    content = [x.strip() for x in content]
    for line in content:
        ioOut.write(line+'\n')
    #
    new_statement(ioOut,"Competitiveness in the Olympics")
    #
    new_slide(ioOut,figName_WHscatter,
              "Mean athletes' Height and Weight for each Olympic sports (only some outliers are marked for clarity).",
             ["For some sports, having the right body type is crucial",
              "Weightlifters are $\sim30$ kg heavier than Rhythmic Gymnasts while of the same height",
              "At the same time, Volleyball players are as heavy as Weightlifters, but are $\sim20$ cm taller"])
    #
    new_slide(ioOut,figName_WHgymnstcsByYear,
              "Mean (black) and gold medalist's (orange) weight and height in Gymnastics. Dashed line is a linear fit to mean values. Missing points are due to missing data.",
             [r"\underline{Example: Gymnastics}",
              r"Notice \textendash\ from $1960$ onward gold medalists are lighter and shorter than the average competitor",
              "Participating athletes gradually became shorter and lighter over the decades, arguably due to the competition",
              "Love gymnastics but haven't got the right body type?.. tough luck"])
    #
    new_slide(ioOut,figName_Maps,
              "Proportion of the total Gold medals ever won by any country, during the Summer (top) and Winter (bottom) Olympics. Proportion of a given country's victories is proportional to the bubble area, with a lower cap at $2\%$.",
             ["Country's climate clearly plays a role in preparing the athletes, providing a competitive advantage or disadvantage",
              "While most countries have won at least one Gold medal during the Summer Olympics, Winter Olympics are dominated by northern countries",
               r"Notice \textendash\ countries from the African and South American continents have never won a Winter Olympics Gold. No snow, no way to practice"])
    #
    #
    new_statement(ioOut,"The End")
    ioOut.write(r'\end{document}\n')
# _| Compile the story.tex (this updates story.pdf)
os.chdir(texPath)
devnull = open(os.devnull, 'w')
subprocess.Popen(['pdflatex', 'story.tex'],stdout=devnull,stderr=devnull)
os.chdir('../')



