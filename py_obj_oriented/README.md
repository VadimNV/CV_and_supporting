<blockquote>
  <p>\| __________________________________________
    <br>/| 
    <br>\| Vadim Nemytov (vadim.nemytov13@imperial.ac.uk),
    <br>/| Imperial College London,
    <br>\| 31-08-2017
    <br>/|
    <br>\| Any of the scripts in this folder are free to use.
    <br>/| __________________________________________
    <br>\|
  </p>
</blockquote>

#### Main workflow:
- ##### the main program is test_classes.py. It uses auxiliary classes and functions to do data analysis and save the resulting histograms in a format compatible with LaTeX (in folder figs_and_TeX you find both the figures and the TeX files)
- ##### The idea is as follows. In my PhD I conduct a computational experiment.
  1. I choose an "interatomic potential"(IP) - this is a model/function that can evaluate a force on every atom for any input configurations of atoms.
  2. I use this IP to do molecular dynamics, i.e. evolve a system of atoms in time.
  3. I repeat these simulations at several temeperatures, e.g. 100K, 300K etc.
  4. At every temperature, I save some frozen atomic configurations, e.g. every 1 picosecond. This creates "snapshots", several at each temperature.
  5. Now, there are several differens IPs. All can evaluate forces on atoms, but some, additionally, calculate extra properties. In our case, some IPs can calculate atomic(ionic) dipole moments, charge transfer or both.
  6. Different IPs can be then used to evaluate forces and other properties on the exact same frozen snapshots, saved previously.
  7. This allows one to study the effect of introducing more complexity into an IP. For example, if we start with an IP that calculate ionic dipole moments and now extend this IP to also calculate charge transfe - what happens?
- ##### classes are written as follows:
  * *computer_experiment* 
    - defines information common to all IPs, e.g. atomic positions of the saved frozen MD snapshots
    - IMPORTANT: maintains state variables (Tk,i) the refer to the "current" snapshot. This is later used and shared by several objects.
  * *IP*, *IPpol*, *IPqeq*, *IPpolQeq* are all classes that caputre information unique to any one IP. In particular, each IP calculates forces on atoms differently, given identical input of atomic configuration. IP class serves as a superclass.
    - IMPORTANT: they are intended to use the state variable (Tk,i) to return "current" properties
  * data_analysis_PolQeq_vs_Pol class creates inside itself three objects - it creates computer_experiment object and then passes it on as an input to IPpolQeq and IPpol objects which are built in such a way that the state variables (Tk,i) are syncronized for all three. This class can then do data post processing and save it as figures that are compatible with LaTeX

#### Auxiliary functions are:
- nn_tree.py - a little code to find nearest neighbours lists for every atom in the simulation box.
- py2tex_fig_env.py - a code that prepares figures in a LaTeX compatible format. This code is almost entirely copy/pasted from http://bkanuka.com/articles/native-latex-plots/
