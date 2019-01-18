#!/usr/bin/env python
from comp_experiment import *

T           = ['100','200','300','500','1000']
filePathDip = "pathOUThistDip/Dip_au_"
filePathF   = "pathOUThistF/force_au_"
filePathQ   = "fort401dir/fort401_"
filePathPos = "pathOUThistF/pos_au_"
filePathCel = "asap_bto_C0vn_in/BaTiO3rhombR3m_3x3x3_"
mdN         = 10
nat         = 135
natUnit     = 27
StringIPqeq = ""
StringIP2   = "AVEq_"

dt_analysis = data_analysis_PolQeq_vs_Pol(filePathPos, filePathCel, T, mdN, nat, natUnit,  # to define computer_experiment object
                                          filePathF, filePathDip, filePathQ,               # to define IPpolQeq            object
                                          filePathF, filePathDip,                          # to define IPpol               object
                                          StringIPqeq,                                     # to define IPpolQeq            object (optional)
                                          StringIP2)                                       # to define IPpol               object (optional)
dt_analysis.setHistVectors()
dt_analysis.saveFig_Pnn_vs_dqTi()
dt_analysis.saveFig_P_vs_dqTi()
dt_analysis.saveFig_Fnn_vs_dqTi()
dt_analysis.saveFig_F_vs_dqTi()
dt_analysis.saveFig_Rnn_vs_dqTi()
dt_analysis.saveFig_RnnStDev_vs_dqTi()
