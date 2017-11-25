#####   ____________________________________________________________________
##### \|                                                                    |/
##### \|<pre>                                                                    </pre>|/
##### /| Vadim Nemytov (vadim.nemytov13@imperial.ac.uk),                    |\
##### \| Imperial College London,                                           |/
##### /| 31-08-2017                                                         |\
##### \|                                                                    |/
##### /| If you use any of the scripts in this folder - please acknowledge. |\
##### \| Please do not use the raw data or figures.                         |/
##### /|____________________________________________________________________|\

##### Main workflow:
- ###### the main program is test_classes.py. It uses auxiliary classes and functions to do data analysis and save the resulting histograms in a format compatible with LaTeX (in folder figs_and_TeX you find both the figures and the TeX files)
- ###### The idea is as follows. In my PhD I conduct a computational experiment. 
1) I choose an "interatomic potential"(IP) - this is a model/function that can evaluate a force on every atom for any input configurations of atoms.
2) I use this IP to do molecular dynamics, i.e. evolve a system of atoms in time.
3) I repeat these simulations at several temeperatures, e.g. 100K, 300K etc.
4) at every temperature, I save some frozen atomic configurations, e.g. every 1 picosecond. This creates "snapshots", several at each temperature.
5) Now, there are several differens IPs. All can evaluate forces on atoms, but some, additionally, calculate extra properties. In our case, some IPs can calculate atomic(ionic) dipole moments, charge transfer or both.
6) different IPs can be then used to evaluate forces and other properties on the exact same frozen snapshots, saved previously. This allows one to study the effect of introducing more complexity into an IP. For example, if we start with an IP that calculate ionic dipole moments and now extend this IP to also calculate charge transfe - what happens?
- ###### classes are written as follows:
1) computer_experiment 
a) defines information common to all IPs, e.g. atomic positions of the saved frozen MD snapshots
b) IMPORTANT: maintains state variables (Tk,i) the refer to the "current" snapshot. This is later used and shared by several objects.
2) IP, IPpol, IPqeq, IPpolQeq are all classes that caputre information unique to any one IP. In particular, each IP calculates forces on atoms differently, given identical input of atomic configuration. IP class serves as a superclass. *IMPORTANT* - they are intended to use the state variable (Tk,i) to return "current" properties
3) data_analysis_PolQeq_vs_Pol class creates inside itself three objects - it creates computer_experiment object and then passes it on as an input to IPpolQeq and IPpol objects which are built in such a way that the state variables (Tk,i) are syncronized for all three. This class can then do data post processing and save it as figures that are compatible with LaTeX

##### Auxiliary functions are:
- nn_tree.py - a little code to find nearest neighbours lists for every atom in the simulation box.
- py2tex_fig_env.py - a code that prepares figures in a LaTeX compatible format. This code is almost entirely copy/pasted from http://bkanuka.com/articles/native-latex-plots/