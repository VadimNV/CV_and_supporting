#!/usr/bin/env python

import math
from numpy import loadtxt
import nn_tree
from py2tex_fig_env import *

class computer_experiment(object):
    # Constructor
    def __init__(self,pathPos,pathCel,T,mdN,nat,natUnit):
        self.T             = T       # set of temperatures, e.g. ['100,'200','300','500,'1000']
        self.mdN           = mdN     # number of saved snapshots from simulation at each temperature (assumed constant) e.g. 10
        self.nat           = nat     # number of atoms (assumed the same at each temperature), e.g. 135
        self.natUnit       = natUnit # smallest (comm. denominator) number of any atomic species. e.g. in [BaTiO3]x2, natUnit = 2, nat = 10 = 2+2+2*3
        self.pathPos       = pathPos # e.g. "pathOUThistF/pos_au_"
        self.pathCel       = pathCel # e.g. "pathOUThistF/pos_au_"
        self.Pos           = []      # intended to give Positions at one fixed T[Tk],i e.g. 200K, snapshot 3
        self.Pos3x3x3      = []      # Positions of ions in a 3x3x3 supercell of the simulation box. Needed to extract distances between nearest neighbours
        self.Cel           = []
        self.current_Tk    = 0       # default Temperature = T[0]
        self.current_i     = 1       # default MD snapshot = 1
        self.NNi_mapd_Ba   = []      # Ba Nearest Neighbours' (NNs') indices mapped back to the simulation cell. To extract NNs' properties, e.g. dipole moments, forces
        self.NNi_mapd_Ti   = []
        self.NNi_mapd_OxTi = []
        self.NNi_mapd_OxBa = []
        self.NNi_Ba        = []      # Ba NNs' indices corresponding to a 3x3x3 supercell of the sim. box (which itself is usually a supercell of the primitive unit cell
        self.NNi_Ti        = []      #                                                                     of the crystal). To extract distance beween nearest neighbours
        self.NNi_OxTi      = []
        self.NNi_OxBa      = []

    # Mutator  (setter) 
    def setPathPos(self,pathP):              # location where atomic positions are stored
        self.pathPos                         = pathP
    def setPathCel(self,pathC):              # location where cell vectors are stored
        self.pathCel                         = pathC
    def set_current_Tk_i(self,in_Tk,in_i):   # these are used to extract current properties, e.g. Pos, Cell, NNind etc.
        global Tk
        global i
        Tk = in_Tk                   # updates global variable value
        i  = in_i                    # updates global variable value
        self.current_Tk                      = Tk
        self.current_i                       = i
    def set_currentPos_Cel_at_Tk_i(self):    # updates self.Pos, self.Cel variables to correspond to snapshot at (Tk,i)
        with open(self.pathPos+self.T[self.current_Tk]+"K_"+str(self.current_i+1)+".dat") as file:
            dataPos  = [[float(digit) for digit in line.split()] for line in file]       
        #
        dataCel  = [[0.0,0.0,0.0] for y in range(0,3)]
        fp = open(self.pathCel+self.T[self.current_Tk]+"K_"+str(self.current_i+1)+".cel")
        for i, line in enumerate(fp):
            if i >=2:
                dataCel[i-2] = [float(digit) for digit in line.split()]
        fp.close()
        dataCel = np.asarray(dataCel)
        #
        self.Pos                             = dataPos
        self.Cel                             = dataCel
    def set_currentNN_Pos27_at_Tk_i(self):   # sets NN indices and constructs Pos27 (in the same loop)
        mpdBa, mpdTi, mpdOxTi, mpdOxBa, Ba, Ti, OxTi, OxBa, dataPos27 = nn_tree.getNNlist(self.pathPos,self.pathCel,self.current_Tk,self.current_i)
        self.NNi_mapd_Ba                     = mpdBa     # Ba Nearest Neighbours' (NNs') indices mapped back to the simulation cell. To extract NNs' properties, e.g. dipole moments, forces
        self.NNi_mapd_Ti                     = mpdTi
        self.NNi_mapd_OxTi                   = mpdOxTi
        self.NNi_mapd_OxBa                   = mpdOxBa
        self.NNi_Ba                          = Ba        # Ba NNs' indices corresponding to a 3x3x3 supercell of the simulation box (which itself is usually a supercell of the primitive unit
        self.NNi_Ti                          = Ti        # cell of the crystal. To extract distance beween nearest neighbours
        self.NNi_OxTi                        = OxTi
        self.NNi_OxBa                        = OxBa
        self.Pos3x3x3                        = dataPos27

    # Accesser (getter)
    def get_currentPos(self):
        return self.Pos
    def get_currentPos3x3x3(self):
        return self.Pos3x3x3
    def get_currentCel(self):
        return self.Cel
    def get_current_Tk_i(self):
        return self.current_Tk, self.current_i
    def get_T(self):
        return self.T
    def get_mdN(self):
        return self.mdN
    def get_natUnit(self):
        return self.natUnit
    def get_nat(self):
        return self.nat
    def get_pathPos(self):
        return self.pathPos
    def get_pathCel(self):
        return self.pathCel
    def get_NN_mapped_Ba(self): 
        return self.NNi_mapd_Ba
    def get_NN_mapped_Ti(self): 
        return self.NNi_mapd_Ti
    def get_NN_mapped_OxTi(self): 
        return self.NNi_mapd_OxTi
    def get_NN_mapped_OxBa(self): 
        return self.NNi_mapd_OxBa
    def get_NN_Ba(self): 
        return self.NNi_Ba
    def get_NN_Ti(self): 
        return self.NNi_Ti
    def get_NN_OxTi(self): 
        return self.NNi_OxTi
    def get_NN_OxBa(self): 
        return self.NNi_OxBa

#-------------------------------- Interatomic Potential(IP) classes.
#                                 IPs can be 1. simple pair-additive that only depend on atomic positions, OR
#                                            2. in addition to 1. depend on ionic dipole moments, OR
#                                            3. in addition to 1. depend on variable ionic charges, OR
#                                            4. in addition to 2. depend on variable ionic charges (so ~2.+3.)

class IP(object):
    # same MD simulation (same trajectories in time and space) but with
    # atomic properties evaluated with a specific Interatomic Potentail (IP)
    # ( assuming BaTiO3 stoichiometry )
    
    # Constructor
    def __init__(self,pathF,comp_experiment_Obj,IP=''):
        if not (IP=='' or IP=='AVEq_' or IP=='FxdFitQ_'):
            if     IP=='AVEq'   :
                IP=='AVEq_'
            elif   IP=='FxdFitQ':
                IP=='FxdFitQ_'
            else                :
                raise TypeError("must pass on IP = '', 'AVEq' or 'FxdFitQ' (not passing IP defaults to '')")       
        self.IP           = IP                      # IP = '', 'AVEq_', 'FxdFitQ_' for QEq=ON, QEq=OFF+ave.q, QEq=OFF+reparametrized, respectively
        self.ceObjPointer = comp_experiment_Obj # now can read/modify variables of an instance of the class 'computer_experiment'. 
                                                    # These variables are then "semi-global", shared among all objects "linked" to comp_experiment_Obj.
        self.Pol          = False
        self.QEq          = False
        self.pathF        = pathF                   # "pathOUThistF/force_au_"
        self.F            = []

    # Mutators (setters)
    #def setCurrent_Tk_i(self,Tk,i):
    #    self.compExpObj.setCurrent_Tk_i(Tk,i) #note, this changes current (Tk,i) globally - for all IP-like objects that were initialized with the same computer_experiment obj as input
    def setCurrentF(self):
        Tk,i = self.ceObjPointer.get_current_Tk_i()
        T    = self.ceObjPointer.get_T()
        with open(self.pathF+T[Tk]+"K_"+self.IP+str(i+1)+".dat") as file:
            data        = [[float(digit) for digit in line.split()] for line in file]
        self.F = data

    # Accessers (getters)
    def getCurrentF(self):
        return self.F

#-----

class IPpol(IP):
    # This IP contains Polarizable Ion model, hence can load dipoles moments from pathDip

    # Constructor
    def __init__(self,pathF,pathDip,comp_experiment_Obj,IP=''):
       super(IPpol,self).__init__(pathF,comp_experiment_Obj,IP)  # see https://stackoverflow.com/questions/38963018/typeerror-super-takes-at-least-1-argument-0-given-error-is-specific-to-any 
                                                                 # for Python 2/3 convention
       self.Pol     = True
       self.QEq     = False
       self.pathDip = pathDip   # "pathOUThistDip/Dip_au_"
       self.Dip     = []

    # Mutators (setters)
    def setCurrentDip(self):
        Tk,i = self.ceObjPointer.get_current_Tk_i()
        T    = self.ceObjPointer.get_T()
        with open(self.pathDip+T[Tk]+"K_"+self.IP+str(i+1)+".dat") as file:
            data        = [[float(digit) for digit in line.split()] for line in file]
        self.Dip = data

    # Accessers (getters)
    def getCurrentDip(self):
        return self.Dip

#-----

class IPqeq(IP):
    # This IP contains Charge Equilibration model (QEq=ON), hence can load charge transfer variables from pathQ

    # Constructor
    def __init__(self,pathF,pathQ,comp_experiment_Obj,IP):
       super(IPqeq,self).__init__(pathF,comp_experiment_Obj,IP)
       self.Pol     = False
       self.QEq     = True
       self.pathQ   = pathQ  # "fort401dir/fort401_"
       self.Q       = []

    # Mutators (setters)
    def setCurrentQ(self):
        Tk,i  = self.ceObjPointer.get_current_Tk_i()
        T     = self.ceObjPointer.get_T()
        dataQ = loadtxt(self.pathQ+T[Tk]+"K_"+self.IP+str(i+1)+".dat")
        self.Q = dataQ

    # Accessers (getters)
    def getCurrentQ(self):
        return self.Q

#-----

class IPpolQeq(IPpol):
    # This IP contains 'polarizable ion' and 'Charge Equilibration'(QEq=ON) models, hence can load charge transfer variables from pathQ
    #import computer_experiment

    # Constructor
    def __init__(self,pathF,pathDip,pathQ,comp_experiment_Obj,IP=''):
       super(IPpolQeq,self).__init__(pathF,pathDip,comp_experiment_Obj,IP)
       self.Pol     = True
       self.QEq     = True
       self.pathQ   = pathQ  # "fort401dir/fort401_"
       self.Q       = []

    # Mutators (setters)
    def setCurrentQ(self):
        Tk,i  = self.ceObjPointer.get_current_Tk_i()
        T     = self.ceObjPointer.get_T()
        dataQ = loadtxt(self.pathQ+T[Tk]+"K_"+self.IP+str(i+1)+".dat")
        self.Q = dataQ

    # Accessers (getters)
    def getCurrentQ(self):
        return self.Q

#--------------------------------
# Recall:
# class computer_experiment    -->    def __init__(self,pathPos,pathCel,T,mdN,nat,natUnit):
# class IPpolQeq               -->    def __init__(self,pathF,pathDip,pathQ,comp_experiment_Obj,IP=''):
# class IPpol                  -->    def __init__(self,pathF,pathDip,comp_experiment_Obj,IP=''):

class data_analysis_PolQeq_vs_Pol(object):
    # -Compare differences in properties of polQEq-type and pol-type potentials vs. charge transfer
    #  i.e., when charge transfer on an ion is large, what does it does this do to local properties?
    #  properties are Forces, Dipoles. Additionally, effect of local structure on the amount of local
    #  charge transfer is also explored.
    # -Note 1: Assuming bulk BaTiO3 system
    # -Note 1: In practice, in my potential at the moment, charge transfer is switched on only for Ti
    #          ions and hence some calculations are made only for Ti. It is easily generalizable

    # Constructor
    def __init__(self,
                 pathPos,pathCel,T,mdN,nat,natUnit,  # to define computer_experiment object
                 pathF1,pathDip1,pathQ1,             # to define IPpolQeq            object
                 pathF2,pathDip2,                    # to define IPpol               object
                 IP1='',                             # to define IPpolQeq            object
                 IP2='AVEq_' ):                      # to define IPpol               object
        # TODO check input variable types:
        # if not ( ... ):
        #     raise TypeError("must pass on ... as input")
        self.comp_experiment   = computer_experiment(pathPos,pathCel,T,mdN,nat,natUnit)           # all three objects
        self.IP_A_qeq          = IPpolQeq(pathF1,pathDip1,pathQ1,self.comp_experiment,IP1)        # are linked to the
        self.IP_B              = IPpol(pathF2,pathDip2,self.comp_experiment,IP2)                  # same current (Tk,i)                                           
        # Forces related variables
        self.FerrAB_Ba         = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        self.FerrAB_Ti         = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        self.FerrAB_Ox         = [[0.0 for x in range(0,mdN*natUnit*3)] for y in range(0,len(T))] # 27+27+27*3 = nat for BaTiO3 x 27 (27=3x3x3 supercell)
        self.nnFaveErrTi_norm  = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        self.nnFaveErrAB_Ti    = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        # Dipoles related variables
        self.PerrAB_Ba         = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        self.PerrAB_Ti         = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        self.PerrAB_Ox         = [[0.0 for x in range(0,mdN*natUnit*3)] for y in range(0,len(T))] # 27+27+27*3 = nat for BaTiO3 x 27 (27=3x3x3 supercell)
        self.nnPaveErrTi_norm  = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        self.nnPaveErrAB_Ti    = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        # Charge Transfer related variables
        self.dqBa              = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        self.dqTi              = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        self.dqOx              = [[0.0 for x in range(0,mdN*natUnit*3)] for y in range(0,len(T))]
        # Distance to NNs related variables
        self.nnRaveErrTi_norm  = [[0.0 for x in range(0,mdN*natUnit)] for y in range(0,len(T))]
        self.nnRaveErrTi_StDev = [[0.0 for x in range(0,mdN*natUnit)] for y in range(0,len(T))]
        
    # Mutators (setters)
    def setHistVectors(self):
        T       = self.comp_experiment.get_T()
        mdN     = self.comp_experiment.get_mdN()
        natUnit = self.comp_experiment.get_natUnit()
        # temporary variables for normalization:
        # Force
        Fmag_Ba = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        Fmag_Ti = [[0.0 for x in range(0,mdN*natUnit)  ] for y in range(0,len(T))]
        Fmag_Ox = [[0.0 for x in range(0,mdN*natUnit*3)] for y in range(0,len(T))]
        FaveBa  = [0.0 for y in range(0,len(T))]
        FaveTi  = [0.0 for y in range(0,len(T))]
        FaveOx  = [0.0 for y in range(0,len(T))]
        # Dipoles - no normalization
        # Charges - to define *change* in charge as deviation from average
        qAveBa  = [0.0 for y in range(0,len(T))]
        qAveTi  = [0.0 for y in range(0,len(T))]
        qAveOx  = [0.0 for y in range(0,len(T))]
        for Tk in range(0,len(T)):
            for i in range(0,mdN):
                # set current Tk and i
                self.comp_experiment.set_current_Tk_i(Tk,i) # IMPORTANT: This updates "current" (Tk,i) for self.computer_experiment, self.IP_A_qeq.ceObj_pointer
                                                            #            and self.IP_A.ceObj_pointer objects. any "getCurrent...()" call will use this (Tk,i) in
                                                            #            all of these three objects
                # hence, now can set current F, Dip, Q, NNindex:
                self.IP_A_qeq.setCurrentF()
                self.IP_B.setCurrentF()
                self.IP_A_qeq.setCurrentDip()
                self.IP_B.setCurrentDip()
                self.IP_A_qeq.setCurrentQ()
                self.comp_experiment.set_currentNN_Pos27_at_Tk_i()
                self.comp_experiment.set_currentPos_Cel_at_Tk_i()
                # Get Forces
                dtA_F       = self.IP_A_qeq.getCurrentF()
                dtB_F       = self.IP_B.getCurrentF()
                # Get Dipoles
                dtA_P       = self.IP_A_qeq.getCurrentDip()
                dtB_P       = self.IP_B.getCurrentDip()
                # Get Charges
                dtA_Q       = self.IP_A_qeq.getCurrentQ()
                # Get List of nearest neighbour indeces, pos3x3x3
                NNindTi     = self.comp_experiment.get_NN_mapped_Ti()
                NNind_np_Ti = self.comp_experiment.get_NN_Ti()
                dataPos     = self.comp_experiment.get_currentPos()
                dataPos27   = self.comp_experiment.get_currentPos3x3x3()
                for j in range(0,natUnit):
                    # ____ ____________
                    #|_Ba_|            \
                    J = j
                    #    --forces  r.m.s
                    Fmag_Ba[Tk][                    j             + i*natUnit  ]  = math.sqrt( (dtA_F[J][0])**2             + (dtA_F[J][1])**2             + (dtA_F[J][2])**2             )
                    self.FerrAB_Ba[Tk][             j             + i*natUnit  ]  = math.sqrt( (dtA_F[J][0]-dtB_F[J][0])**2 + (dtA_F[J][1]-dtB_F[J][1])**2 + (dtA_F[J][2]-dtB_F[J][2])**2 )
                    #    --dipoles r.m.s
                    self.PerrAB_Ba[Tk][             j             + i*natUnit  ]  = math.sqrt( (dtA_P[J][0]-dtB_P[J][0])**2 + (dtA_P[J][1]-dtB_P[J][1])**2 + (dtA_P[J][2]-dtB_P[J][2])**2 )
                    #    --charges
                    self.dqBa[Tk][                  j             + i*natUnit  ]  = dtA_Q[J]
                    #__________________/
                    # ____ ____________
                    #|_Ti_|            \
                    J = j+natUnit
                    #    --force   r.m.s
                    Fmag_Ti[Tk][                    j             + i*natUnit  ]  = math.sqrt( (dtA_F[J][0])**2             + (dtA_F[J][1])**2             + (dtA_F[J][2])**2             )
                    self.FerrAB_Ti[Tk][             j             + i*natUnit  ]  = math.sqrt( (dtA_F[J][0]-dtB_F[J][0])**2 + (dtA_F[J][1]-dtB_F[J][1])**2 + (dtA_F[J][2]-dtB_F[J][2])**2 )
                    #    --forces of its nearest neighbours
                    for l in range(0,len(NNindTi[j])):
                        S = NNindTi[j][l]
                        self.nnFaveErrAB_Ti[Tk][    j             + i*natUnit  ] += math.sqrt( (dtA_F[S][0]-dtB_F[S][0])**2 + (dtA_F[S][1]-dtB_F[S][1])**2 + (dtA_F[S][2]-dtB_F[S][2])**2 )/len(NNindTi[j])
                        self.nnFaveErrTi_norm[Tk][  j             + i*natUnit  ] += math.sqrt( (dtA_F[S][0])**2             + (dtA_F[S][1])**2             + (dtA_F[S][2])**2             )/len(NNindTi[j])
                    #    --dipoles r.m.s
                    self.PerrAB_Ti[Tk][             j             + i*natUnit  ]  = math.sqrt( (dtA_P[J][0]-dtB_P[J][0])**2 + (dtA_P[J][1]-dtB_P[J][1])**2 + (dtA_P[J][2]-dtB_P[J][2])**2 )
                    #    --dipoles of its nearest neighbours
                    for l in range(0,len(NNindTi[j])):
                        S = NNindTi[j][l]
                        self.nnPaveErrAB_Ti[Tk][    j             + i*natUnit  ] += math.sqrt( (dtA_P[S][0]-dtB_P[S][0])**2 + (dtA_P[S][1]-dtB_P[S][1])**2 + (dtA_P[S][2]-dtB_P[S][2])**2 )/len(NNindTi[j])
                        self.nnPaveErrTi_norm[Tk][  j             + i*natUnit  ] += math.sqrt( (dtA_P[S][0])**2             + (dtA_P[S][1])**2             + (dtA_P[S][2])**2             )/len(NNindTi[j])
                    #    --charges
                    self.dqTi[Tk][                  j             + i*natUnit  ]  = dtA_Q[J]
                    #    --Rij of its nearest neighbours
                    for l in range(0,len(NNindTi[j])):
                        # mean Rnn
                        S = NNind_np_Ti[j][l] # notice, we are using *UNmapped* indices, i.e. those that point to Pos3x3x3
                        Rij = np.asarray(dataPos27[S]) - np.asarray(dataPos[J])
                        self.nnRaveErrTi_norm[Tk][  j             + i*natUnit  ] += math.sqrt( (Rij[0])**2                  + (Rij[1])**2                  + (Rij[2])**2                  )/len(NNindTi[j])
                    for l in range(0,len(NNindTi[j])):
                        # standard deviation of Rnn
                        S = NNind_np_Ti[j][l] # notice, we are using *UNmapped* indices, i.e. those that point to Pos3x3x3
                        Rij = np.asarray(dataPos27[S]) - np.asarray(dataPos[J])
                        self.nnRaveErrTi_StDev[Tk][ j             + i*natUnit  ] +=(math.sqrt( (Rij[0])**2 + (Rij[1])**2 + (Rij[2])**2) - self.nnRaveErrTi_norm[Tk][j+i*natUnit])**2
                    self.nnRaveErrTi_StDev[Tk][     j             + i*natUnit  ]  = math.sqrt( self.nnRaveErrTi_StDev[Tk][j + i*natUnit]/(len(NNindTi[j])-1))
                    #__________________/
                    # _____ ___________
                    #|_Ox3_|           \
                    J = j+natUnit*2
                    #    --force   r.m.s (1)
                    Fmag_Ox[Tk][                    j             + i*natUnit*3]  = math.sqrt( (dtA_F[J][0])**2             + (dtA_F[J][1])**2             + (dtA_F[J][2])**2             )
                    self.FerrAB_Ox[Tk][             j             + i*natUnit*3]  = math.sqrt( (dtA_F[J][0]-dtB_F[J][0])**2 + (dtA_F[J][1]-dtB_F[J][1])**2 + (dtA_F[J][2]-dtB_F[J][2])**2 )
                    #    --dipoles r.m.s (1)
                    self.PerrAB_Ox[Tk][             j             + i*natUnit*3]  = math.sqrt( (dtA_P[J][0]-dtB_P[J][0])**2 + (dtA_P[J][1]-dtB_P[J][1])**2 + (dtA_P[J][2]-dtB_P[J][2])**2 )
                    #    --charges       (1)
                    self.dqOx[Tk][                  j             + i*natUnit*3]  = dtA_Q[J]
                    J = J+natUnit
                    #    --force   r.m.s (2)
                    Fmag_Ox[Tk][                    j + natUnit   + i*natUnit*3]  = math.sqrt( (dtA_F[J][0])**2             + (dtA_F[J][1])**2             + (dtA_F[J][2])**2             )
                    self.FerrAB_Ox[Tk][             j + natUnit   + i*natUnit*3]  = math.sqrt( (dtA_F[J][0]-dtB_F[J][0])**2 + (dtA_F[J][1]-dtB_F[J][1])**2 + (dtA_F[J][2]-dtB_F[J][2])**2 )
                    #    --dipoles r.m.s (2)
                    self.PerrAB_Ox[Tk][             j + natUnit   + i*natUnit*3]  = math.sqrt( (dtA_P[J][0]-dtB_P[J][0])**2 + (dtA_P[J][1]-dtB_P[J][1])**2 + (dtA_P[J][2]-dtB_P[J][2])**2 )
                    #    --charges       (2)
                    self.dqOx[Tk][                  j + natUnit   + i*natUnit*3]  = dtA_Q[J]
                    J = J+natUnit
                    #    --force   r.m.s (3)
                    Fmag_Ox[Tk][                    j + natUnit*2 + i*natUnit*3]  = math.sqrt( (dtA_F[J][0])**2             + (dtA_F[J][1])**2             + (dtA_F[J][2])**2             )
                    self.FerrAB_Ox[Tk][             j + natUnit*2 + i*natUnit*3]  = math.sqrt( (dtA_F[J][0]-dtB_F[J][0])**2 + (dtA_F[J][1]-dtB_F[J][1])**2 + (dtA_F[J][2]-dtB_F[J][2])**2 )
                    #    --dipoles r.m.s (3)
                    self.PerrAB_Ox[Tk][             j + natUnit*2 + i*natUnit*3]  = math.sqrt( (dtA_P[J][0]-dtB_P[J][0])**2 + (dtA_P[J][1]-dtB_P[J][1])**2 + (dtA_P[J][2]-dtB_P[J][2])**2 )
                    #    --charges       (3)
                    self.dqOx[Tk][                  j + natUnit*2 + i*natUnit*3]  = dtA_Q[J]
                    #__________________/
            qAveBa[Tk] = np.average(self.dqBa[Tk][:])
            qAveTi[Tk] = np.average(self.dqTi[Tk][:])
            qAveOx[Tk] = np.average(self.dqOx[Tk][:])
            FaveBa[Tk] = np.average(Fmag_Ba[Tk][:])
            FaveTi[Tk] = np.average(Fmag_Ti[Tk][:])
            FaveOx[Tk] = np.average(Fmag_Ox[Tk][:])
            # define *change* in charge as deviation from average:
            self.dqBa[Tk]   = [x-qAveBa[Tk] for x in self.dqBa[Tk]]
            self.dqTi[Tk]   = [x-qAveTi[Tk] for x in self.dqTi[Tk]]
            self.dqOx[Tk]   = [x-qAveOx[Tk] for x in self.dqOx[Tk]]
            # normalize on-site forces by average for that specie:
            self.FerrAB_Ti[Tk]      = [x/FaveTi[Tk] for x in self.FerrAB_Ti[Tk]]
            # normalize NNs' forces by average for NN specie:
            self.nnFaveErrAB_Ti[Tk] = [x/FaveOx[Tk] for x in self.nnFaveErrAB_Ti[Tk]] # Note !!! NNs of Ti are Oxygens, hence dividing by FaveOx[Tk]

    # Note to GitHub readers: all data-vizualisation was subsequently moved to a separt Python library, and was called from here.
    #                         Final version of this file is big and is less illustrative, so not shown.
    def saveFig_F_vs_dqTi(self):                                       # TODO, all safeFig_...() are almost identical -> write a function, call it in each saveFig...()
        # |||\\ Make a 2D Histogram (Py-to-LaTeX) //|||
        xmin, xmax  = -0.08, 0.08                                      # TODO set variable, same for all figs ~ -max(Abs(dqTi[:])), max(Abs(dqTi[:]))
        ymin, ymax  =  0.0, 0.27                                       # 0.0, max(FerrAveQti[0])
        dqBinSize   = [0.0105, 0.011, 0.014, 0.018, 0.020]             # TODO set variable, same for all figs
        FerrBinSize = 0.013                                            # have to play around with this parameter
        T           = self.comp_experiment.get_T()
        for Tk in range(0,len(T)):
            figTk, ax  = newfigTall(0.45)                              # this will be a subfigure in LaTeX, taking up 0.45 pagewidth
            rang = [[xmin, xmax], [ymin, ymax]]
            dqBinNum   = int((xmax - xmin) / dqBinSize[Tk])
            FerrBinNum = int((ymax - ymin) / FerrBinSize )
            binsxy     = [dqBinNum,FerrBinNum] 
            H, xedges, yedges = np.histogram2d(self.dqTi[Tk], self.FerrAB_Ti[Tk], range=rang, bins=binsxy)
            extent     = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
            #    --find average Ferr for each dq bin
            i_ave        = [0.0 for x in range(0,dqBinNum)]
            FerrTi_ave   = [0.0 for x in range(0,dqBinNum)]
            xCenters     = [0.0 for x in range(0,dqBinNum)]
            countNotZero = 0
            indNotZero   = [1000000 for x in range(0,dqBinNum)]
            for j in range(0,dqBinNum):
                for i in range(0,FerrBinNum):
                    i_ave[j] = i_ave[j] + 1.0*i*H[j][i]
                if np.sum(H[j][:])>0.0 :
                    i_ave[j]      = i_ave[j]/np.sum(H[j][:])
                    countNotZero  = countNotZero + 1
                    indNotZero[j] = j
                FerrTi_ave[j] = ymin + (ymax-ymin)*i_ave[j]/FerrBinNum
                xCenters[j]   = (xedges[j] + xedges[j+1])/2.0
            FerrTi_ave_NotZero = [0.0 for x in range(0,countNotZero)]
            xCenters_NotZero   = [0.0 for x in range(0,countNotZero)]
            ii = 0
            for j in range(0,dqBinNum):
                if indNotZero[j] < 1000000 :
                    FerrTi_ave_NotZero[ii] = FerrTi_ave[j]
                    xCenters_NotZero[ii]   = xCenters[j]
                    ii = ii + 1
            #    --now plot
            cp = ax.imshow(H.transpose()[::-1], interpolation='nearest', extent=extent, cmap=cm.jet,vmin=0.0,vmax=24.0)
            plt.scatter(xCenters_NotZero,FerrTi_ave_NotZero,color='pink',figure=figTk)
            figTk.colorbar(cp,fraction=0.075, pad=0.04)
            savefig('figs_and_TeX/Ferr_vs_dq_Ti_'+T[Tk]+'K')
            closefig(figTk)
    def saveFig_Fnn_vs_dqTi(self):
        # |||\\ Make a 2D Histogram (Py-to-LaTeX) //|||
        xmin, xmax  = -0.08, 0.08                                      # TODO set variable, same for all figs ~ -max(Abs(dqTi[:])), max(Abs(dqTi[:])) min(dqTi[0]), max(dqTi[0])
        ymin, ymax  =  0.0, max([max(l) for l in self.nnFaveErrAB_Ti]) # 0.0, max(FerrAveQti[0])                                                      0.025  # 0.0, max(FerrAveQti[0])
        dqBinSize   = [0.0105, 0.011, 0.014, 0.018, 0.020]             # TODO set variable, same for all figs
        FerrBinSize = 0.013                                            # have to play around with this parameter
        T           = self.comp_experiment.get_T()                                                                                                  
        for Tk in range(0,len(T)):                                                                                                                  
            figTk, ax  = newfigTall(0.45)                              # this will be a subfigure in LaTeX, taking up 0.45 pagewidth
            rang = [[xmin, xmax], [ymin, ymax]]
            dqBinNum   = int((xmax - xmin) / dqBinSize[Tk])
            FerrBinNum = int((ymax - ymin) / FerrBinSize )
            binsxy     = [dqBinNum,FerrBinNum] 
            H, xedges, yedges = np.histogram2d(self.dqTi[Tk], self.nnFaveErrAB_Ti[Tk], range=rang, bins=binsxy)
            extent     = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
            #    --find average Ferr for each dq bin
            i_ave        = [0.0 for x in range(0,dqBinNum)]
            nnFerrTi_ave   = [0.0 for x in range(0,dqBinNum)]
            xCenters     = [0.0 for x in range(0,dqBinNum)]
            countNotZero = 0
            indNotZero   = [1000000 for x in range(0,dqBinNum)]
            for j in range(0,dqBinNum):
                for i in range(0,FerrBinNum):
                    i_ave[j] = i_ave[j] + 1.0*i*H[j][i]
                if np.sum(H[j][:])>0.0 :
                    i_ave[j]      = i_ave[j]/np.sum(H[j][:])
                    countNotZero  = countNotZero + 1
                    indNotZero[j] = j
                nnFerrTi_ave[j] = ymin + (ymax-ymin)*i_ave[j]/FerrBinNum
                xCenters[j]   = (xedges[j] + xedges[j+1])/2.0
            nnFerrTi_ave_NotZero = [0.0 for x in range(0,countNotZero)]
            xCenters_NotZero   = [0.0 for x in range(0,countNotZero)]
            ii = 0
            for j in range(0,dqBinNum):
                if indNotZero[j] < 1000000 :
                    nnFerrTi_ave_NotZero[ii] = nnFerrTi_ave[j]
                    xCenters_NotZero[ii]   = xCenters[j]
                    ii = ii + 1
            #    --now plot
            cp = ax.imshow(H.transpose()[::-1], interpolation='nearest', aspect='auto', extent=extent, cmap=cm.jet, vmin=0.0, vmax=42.5)
            figTk.colorbar(cp)
            plt.scatter(xCenters_NotZero,nnFerrTi_ave_NotZero,color='pink',figure=figTk)
            savefig('figs_and_TeX/FerrNN_vs_dq_Ti_'+T[Tk]+'K')
            closefig(figTk)
    def saveFig_P_vs_dqTi(self):
        # |||\\ Make a 2D Histogram (Py-to-LaTeX) //|||
        xmin, xmax  = -0.08, 0.08                                      # TODO set variable, same for all figs ~ -max(Abs(dqTi[:])), max(Abs(dqTi[:])) min(dqTi[0]), max(dqTi[0])
        ymin, ymax  =  0.0, 1.0                                        # max([max(l) for l in PerrAveQti]) # 1.0  # 0.0, max(PerrAveQti[0])
        dqBinSize   = [0.0105, 0.011, 0.014, 0.018, 0.020]             # TODO set variable, same for all figs
        PerrBinSize = 0.03                                             # have to play around with this parameter
        T           = self.comp_experiment.get_T()
        for Tk in range(0,len(T)):
            figTk, ax  = newfigTall(0.45)                              # this will be a subfigure in LaTeX, taking up 0.45 pagewidth
            rang = [[xmin, xmax], [ymin, ymax]]
            dqBinNum   = int((xmax - xmin) / dqBinSize[Tk])
            PerrBinNum = int((ymax - ymin) / PerrBinSize )
            binsxy     = [dqBinNum,PerrBinNum] 
            H, xedges, yedges = np.histogram2d(self.dqTi[Tk], self.PerrAB_Ti[Tk], range=rang, bins=binsxy)
            extent     = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
            #    --find average Perr for each dq bin
            i_ave        = [0.0 for x in range(0,dqBinNum)]
            PerrTi_ave   = [0.0 for x in range(0,dqBinNum)]
            xCenters     = [0.0 for x in range(0,dqBinNum)]
            countNotZero = 0
            indNotZero   = [1000000 for x in range(0,dqBinNum)]
            for j in range(0,dqBinNum):
                for i in range(0,PerrBinNum):
                    i_ave[j] = i_ave[j] + 1.0*i*H[j][i]
                if np.sum(H[j][:])>0.0 :
                    i_ave[j]      = i_ave[j]/np.sum(H[j][:])
                    countNotZero  = countNotZero + 1
                    indNotZero[j] = j
                PerrTi_ave[j] = ymin + (ymax-ymin)*i_ave[j]/PerrBinNum
                xCenters[j]   = (xedges[j] + xedges[j+1])/2.0
            PerrTi_ave_NotZero = [0.0 for x in range(0,countNotZero)]
            xCenters_NotZero   = [0.0 for x in range(0,countNotZero)]
            ii = 0
            for j in range(0,dqBinNum):
                if indNotZero[j] < 1000000 :
                    PerrTi_ave_NotZero[ii] = PerrTi_ave[j]
                    xCenters_NotZero[ii]   = xCenters[j]
                    ii = ii + 1
            #    --now plot
            cp = ax.imshow(H.transpose()[::-1], interpolation='nearest', aspect='auto', extent=extent, cmap=cm.jet, vmin=0.0, vmax=13.0)
            figTk.colorbar(cp)
            plt.scatter(xCenters_NotZero,PerrTi_ave_NotZero,color='pink',figure=figTk)
            savefig('figs_and_TeX/Perr_vs_dq_Ti_'+T[Tk]+'K')
            closefig(figTk)
    def saveFig_Pnn_vs_dqTi(self):
        # |||\\ Make a 2D Histogram (Py-to-LaTeX) //|||
        xmin, xmax  = -0.08, 0.08                                      # TODO set variable, same for all figs ~ -max(Abs(dqTi[:])), max(Abs(dqTi[:])) min(dqTi[0]), max(dqTi[0]))
        ymin, ymax  =  0.0, 0.5                                        # max([max(l) for l in PerrAveQti]) # 1.0  # 0.0, max(PerrAveQti[0])
        dqBinSize   = [0.0105, 0.011, 0.014, 0.018, 0.020]             # TODO set variable, same for all figs
        PerrBinSize = 0.0167                                           # have to play around with this parameter
        T           = self.comp_experiment.get_T()
        for Tk in range(0,len(T)):                                                                                                                                               
            figTk, ax  = newfigTall(0.45)                              # this will be a subfigure in LaTeX, taking up 0.45 pagewidth
            rang = [[xmin, xmax], [ymin, ymax]]
            dqBinNum   = int((xmax - xmin) / dqBinSize[Tk])
            PerrBinNum = int((ymax - ymin) / PerrBinSize )
            binsxy     = [dqBinNum,PerrBinNum] 
            H, xedges, yedges = np.histogram2d(self.dqTi[Tk], self.nnPaveErrAB_Ti[Tk], range=rang, bins=binsxy)
            extent     = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
            #    --find average Perr for each dq bin
            i_ave        = [0.0 for x in range(0,dqBinNum)]
            nnPerrTi_ave = [0.0 for x in range(0,dqBinNum)]
            xCenters     = [0.0 for x in range(0,dqBinNum)]
            countNotZero = 0
            indNotZero   = [1000000 for x in range(0,dqBinNum)]
            for j in range(0,dqBinNum):
                for i in range(0,PerrBinNum):
                    i_ave[j] = i_ave[j] + 1.0*i*H[j][i]
                if np.sum(H[j][:])>0.0 :
                    i_ave[j]      = i_ave[j]/np.sum(H[j][:])
                    countNotZero  = countNotZero + 1
                    indNotZero[j] = j
                nnPerrTi_ave[j] = ymin + (ymax-ymin)*i_ave[j]/PerrBinNum
                xCenters[j]   = (xedges[j] + xedges[j+1])/2.0
            nnPerrTi_ave_NotZero = [0.0 for x in range(0,countNotZero)]
            xCenters_NotZero   = [0.0 for x in range(0,countNotZero)]
            ii = 0
            for j in range(0,dqBinNum):
                if indNotZero[j] < 1000000 :
                    nnPerrTi_ave_NotZero[ii] = nnPerrTi_ave[j]
                    xCenters_NotZero[ii]   = xCenters[j]
                    ii = ii + 1
            #    --now plot
            cp = ax.imshow(H.transpose()[::-1], interpolation='nearest', aspect='auto', extent=extent, cmap=cm.jet, vmin=0.0, vmax=18.0)
            figTk.colorbar(cp)
            plt.scatter(xCenters_NotZero,nnPerrTi_ave_NotZero,color='pink',figure=figTk)
            savefig('figs_and_TeX/PerrNN_vs_dq_Ti_'+T[Tk]+'K')
            closefig(figTk)
    def saveFig_Rnn_vs_dqTi(self):
        xmin, xmax  = -0.08, 0.08 # min(dqTi[0]), max(dqTi[0])
        ymin, ymax  =  min([min(l) for l in self.nnRaveErrTi_norm]) - 0.1, max([max(l) for l in self.nnRaveErrTi_norm])+0.1 # 0.025  # 0.0, max(FerrAveQti[0])
        dqBinSize   = [0.0105, 0.011, 0.014, 0.018, 0.020]
        RerrBinSize = 0.015
        T           = self.comp_experiment.get_T()
        for Tk in range(0,len(T)):
            figTk, ax  = newfigTall(0.45)
            rang = [[xmin, xmax], [ymin, ymax]]
            dqBinNum   = int((xmax - xmin) / dqBinSize[Tk])
            RerrBinNum = int((ymax - ymin) / RerrBinSize )
            binsxy     = [dqBinNum,RerrBinNum] 
            H, xedges, yedges = np.histogram2d(self.dqTi[Tk], self.nnRaveErrTi_norm[Tk], range=rang, bins=binsxy)
            extent     = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
            #    --find average Ferr for each dq bin
            i_ave        = [0.0 for x in range(0,dqBinNum)]
            nnRerrTi_ave   = [0.0 for x in range(0,dqBinNum)]
            xCenters     = [0.0 for x in range(0,dqBinNum)]
            countNotZero = 0
            indNotZero   = [1000000 for x in range(0,dqBinNum)]
            for j in range(0,dqBinNum):
                for i in range(0,RerrBinNum):
                    i_ave[j] = i_ave[j] + 1.0*i*H[j][i]
                if np.sum(H[j][:])>0.0 :
                    i_ave[j]      = i_ave[j]/np.sum(H[j][:])
                    countNotZero  = countNotZero + 1
                    indNotZero[j] = j
                nnRerrTi_ave[j] = ymin + (ymax-ymin)*i_ave[j]/RerrBinNum
                xCenters[j]   = (xedges[j] + xedges[j+1])/2.0
            nnRerrTi_ave_NotZero = [0.0 for x in range(0,countNotZero)]
            xCenters_NotZero   = [0.0 for x in range(0,countNotZero)]
            ii = 0
            for j in range(0,dqBinNum):
                if indNotZero[j] < 1000000 :
                    nnRerrTi_ave_NotZero[ii] = nnRerrTi_ave[j]
                    xCenters_NotZero[ii]   = xCenters[j]
                    ii = ii + 1
            #    --now plot
            cp = ax.imshow(H.transpose()[::-1], interpolation='nearest', aspect='auto', extent=extent, cmap=cm.jet, vmin=0.0, vmax=55.0)
            figTk.colorbar(cp)
            plt.scatter(xCenters_NotZero,nnRerrTi_ave_NotZero,color='pink',figure=figTk)
            #plt.savefig('Rerr_vs_dq_Ti_'+T[Tk]+'K.png',figure=figTk)
            savefig('figs_and_TeX/RnnNorm_vs_dq_Ti_'+T[Tk]+'K') # ~ * NEW * ~
            closefig(figTk)
    
    def saveFig_RnnStDev_vs_dqTi(self):
        xmin, xmax  = -0.08, 0.08 # min(dqTi[0]), max(dqTi[0])
        ymin, ymax  =  min([min(l) for l in self.nnRaveErrTi_StDev]) - 0.1, max([max(l) for l in self.nnRaveErrTi_StDev])+0.1 # 0.025  # 0.0, max(FerrAveQti[0])
        dqBinSize   = [0.0105, 0.011, 0.014, 0.018, 0.020]
        RerrBinSize = 0.015
        T           = self.comp_experiment.get_T()
        for Tk in range(0,len(T)):
            figTk, ax  = newfigTall(0.45)
            rang = [[xmin, xmax], [ymin, ymax]]
            dqBinNum   = int((xmax - xmin) / dqBinSize[Tk])
            RerrBinNum = int((ymax - ymin) / RerrBinSize )
            binsxy     = [dqBinNum,RerrBinNum] 
            H, xedges, yedges = np.histogram2d(self.dqTi[Tk], self.nnRaveErrTi_StDev[Tk], range=rang, bins=binsxy)
            extent     = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
            #    --find average Ferr for each dq bin
            i_ave        = [0.0 for x in range(0,dqBinNum)]
            nnRerrTi_ave   = [0.0 for x in range(0,dqBinNum)]
            xCenters     = [0.0 for x in range(0,dqBinNum)]
            countNotZero = 0
            indNotZero   = [1000000 for x in range(0,dqBinNum)]
            for j in range(0,dqBinNum):
                for i in range(0,RerrBinNum):
                    i_ave[j] = i_ave[j] + 1.0*i*H[j][i]
                if np.sum(H[j][:])>0.0 :
                    i_ave[j]      = i_ave[j]/np.sum(H[j][:])
                    countNotZero  = countNotZero + 1
                    indNotZero[j] = j
                nnRerrTi_ave[j] = ymin + (ymax-ymin)*i_ave[j]/RerrBinNum
                xCenters[j]   = (xedges[j] + xedges[j+1])/2.0
            nnRerrTi_ave_NotZero = [0.0 for x in range(0,countNotZero)]
            xCenters_NotZero   = [0.0 for x in range(0,countNotZero)]
            ii = 0
            for j in range(0,dqBinNum):
                if indNotZero[j] < 1000000 :
                    nnRerrTi_ave_NotZero[ii] = nnRerrTi_ave[j]
                    xCenters_NotZero[ii]   = xCenters[j]
                    ii = ii + 1
            #    --now plot
            cp = ax.imshow(H.transpose()[::-1], interpolation='nearest', aspect='auto', extent=extent, cmap=cm.jet, vmin=0.0, vmax=19.0)
            figTk.colorbar(cp)
            plt.scatter(xCenters_NotZero,nnRerrTi_ave_NotZero,color='pink',figure=figTk)
            savefig('figs_and_TeX/RnnStDev_vs_dq_Ti_'+T[Tk]+'K')
            closefig(figTk)
