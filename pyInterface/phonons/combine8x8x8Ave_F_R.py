# combining averages, MUST:
#  1. all be for the same number of atoms, same supercell
#  2. all use the same time step


#
pathHome    = '/home/vadim/Documents/PhD_weekly_on_GitLab/PhD_Weekly_Desktop/PhD_Thesis/final_data/atT_phonons/'
path_md     = '/home/vadim/workspace/ASAP_runningCode/Examples/Traj/12_bto_2018_lowT_R3m/qeqON_polON/100K/8x8x8/'  # qeqON_polON/100K/'
#path_md     = '/home/vadim/workspace/ASAP_runningCode/Examples/Traj/12_bto_2018_lowT_R3m/qeqON_polON/100K/8x8x8_b/'  # *** ^^^ qeqON_polON/100K/'
#path_md     = '/home/vadim/workspace/ASAP_runningCode/Examples/Traj/12_bto_2018_lowT_R3m/qeqON_polON/100K/8x8x8_c/'  # *** ^^^ qeqON_polON/100K/'
#path_md     = '/home/vadim/workspace/ASAP_runningCode/Examples/Traj/12_bto_2018_lowT_R3m/qeqON_polON/100K/8x8x8_d/'  # *** ^^^ qeqON_polON/100K/'
#path_md     = '/home/vadim/workspace/ASAP_runningCode/Examples/Traj/12_bto_2018_lowT_R3m/qeqON_polON/100K/8x8x8_e/'  # *** ^^^ qeqON_polON/100K/'
#path_md     = '/home/vadim/workspace/ASAP_runningCode/Examples/Traj/12_bto_2018_lowT_R3m/qeqON_polON/100K/8x8x8_f/'  # *** ^^^ qeqON_polON/100K/'
fGen        = 'disp_out/s5_out/gen_bto_100K_fR_Sdisp.in'
fDISP       = 'disp_out/s5_out/DISP'
t_step      = 10
#
#calc_ind_ls   = ['_a_s4_', '_b_s4_', '_c_s4_', '_d_s4_', '_e_s4_', '_f_s4_']
#ave_num_ls    = [1100    , 1100    , 1100    , 900     , 900     , 900     ]
#calc_ind_ls   = ['_a_s4_', '_d_s4_']
#ave_num_ls    = [1100    , 900     ]
#calc_ind_ls   = ['_b_s4_', '_c_s4_', '_e_s4_', '_f_s4_']
#ave_num_ls    = [1100    , 1100    , 900     , 900     ]
calc_ind_ls   = ['_b_s4_', '_f_s4_']
ave_num_ls    = [1100    , 900     ]
ave_num       = sum(ave_num_ls)
pathAv_s_F_ls = [pathHome+'bto/all_aveSameMD_s_F/aveSameMD100_s_F_qeqOn8x8x8'+str(i)+'out' for i in calc_ind_ls ]
#pathAv_s_F_ls = [pathHome+'bto/all_aveSameMD_s_F/aveSameMD20_s_F_qeqOn8x8x8'+str(i)+'out' for i in calc_ind_ls ]
#pathAv_s_F_ls = [pathHome+'bto/all_aveSameMD_s_F/aveSameMD10_s_F_qeqOn8x8x8'+str(i)+'out' for i in calc_ind_ls ]
#
nat         = 2560 # 320 # 1080 # 135
natUnit     = nat/(1+1+3)
auTOang     = 0.5291772108                     # as in ASAP
auTOang3unit= auTOang*auTOang*auTOang/(nat/5)  # Ang**3 per BaTiO3
#

#  | read how many displacements are made (e.g. for nxnxn system 3 displacements, each applied to first atom of each specie, to Ba, to Ti, to Ox)
# _|      how many scaling factors are used
ndisp_sc    = 0
scale_i     = []
with open(path_md+fGen) as ioGen:
    content = ioGen.readlines()
    content = [x.strip() for x in content]
    for ii,lineG in enumerate(content):
        if 'displacement_list_phon' in lineG.split():
            ndisp    = int(lineG.split()[-1])
        elif 'disp_scale'           in lineG.split():
            ndisp_sc = int(lineG.split()[-1])
            if ndisp_sc > 0:
                for sc in content[ii+1].split():
                    scale_i.append(float(sc))
    if ndisp_sc == 0:
        ndisp_sc = 1
        scale_i.append(1.0)

# _| read index of displaced atoms
disp_i = []
with open(path_md+fDISP) as ioDISP:
    content = ioDISP.readlines()
    content = [x.strip() for x in content]
    for lineD in content:
        disp_i.append(int(lineD.split()[0]))

# _| combine averages for forces and positions
s_ave     = [[[[0.,0.,0.] for jj in range(0,nat)] for i in range(0,ndisp)] for j in range(0,ndisp_sc)] # s_ave[j][i][atm_n] ~ disp_i, scale_factor_j, atom_n
f_ave     = [[[[0.,0.,0.] for jj in range(0,nat)] for i in range(0,ndisp)] for j in range(0,ndisp_sc)] # f_ave[j][i][atm_n] ~ disp_i, scale_factor_j, atom_n
fOut_sAve = pathHome+'bto/cmbd_ave_s_F/s_Ave'+str(ave_num)+'_'+str(t_step)+'tstep_disp_'        # ending 1_sc_1, 2_sc_1, 3_sc_1
fOut_fAve = pathHome+'bto/cmbd_ave_s_F/force_au_ave'+str(ave_num)+'_'+str(t_step)+'tstep_disp_'        # ending 1_sc_1, 2_sc_1, 3_sc_1
for i in range(0,ndisp):
    iF = i + 1
    for j in range(0,ndisp_sc):
        jF = j + 1
        for clc_ii,clcI in enumerate(calc_ind_ls):
            factor_ave = float(ave_num_ls[clc_ii])/float(ave_num)
            fIn_fAve = pathAv_s_F_ls[clc_ii]+'/force_au_ave'+str(ave_num_ls[clc_ii])+'_'+str(t_step)+'tstep_disp_'+str(iF)+'_sc_'+str(jF)  # ending 1_sc_1, 2_sc_1, 3_sc_1
            fIn_sAve = pathAv_s_F_ls[clc_ii]+'/s_Ave'+str(ave_num_ls[clc_ii])+'_'+str(t_step)+'tstep_disp_'+str(iF)+'_sc_'+str(jF)  # ending 1_sc_1, 2_sc_1, 3_sc_1
            with open(fIn_sAve) as ioIn_sAve, open(fIn_fAve) as ioIn_fAve:
                content_s = ioIn_sAve.readlines()
                content_s = [x.strip() for x in content_s]
                content_f = ioIn_fAve.readlines()
                content_f = [x.strip() for x in content_f]
                for ii,(line_s,line_f) in enumerate(zip(content_s,content_f)):
                    this_s_av = [float(x) for x in line_s.split()]
                    s_ave[j][i][ii][0] += this_s_av[0]*factor_ave
                    s_ave[j][i][ii][1] += this_s_av[1]*factor_ave
                    s_ave[j][i][ii][2] += this_s_av[2]*factor_ave
                    this_f_av = [float(x) for x in line_f.split()]
                    f_ave[j][i][ii][0] += this_f_av[0]*factor_ave
                    f_ave[j][i][ii][1] += this_f_av[1]*factor_ave
                    f_ave[j][i][ii][2] += this_f_av[2]*factor_ave
        # ...can now write to file
        with open(fOut_sAve+str(iF)+'_sc_'+str(jF),'w') as ioOut_sAve_i_j, open(fOut_fAve+str(iF)+'_sc_'+str(jF),'w') as ioOut_fAve_i_j:
            for s_ij,f_ij in zip(s_ave[j][i],f_ave[j][i]):
                ioOut_sAve_i_j.write(str(s_ij[0])+'    '+str(s_ij[1])+'    '+str(s_ij[2])+'\n')
                ioOut_fAve_i_j.write(str(f_ij[0])+'    '+str(f_ij[1])+'    '+str(f_ij[2])+'\n')

# _| combine averages in the info file
P_T_V_ave     = [ 0.0, 0.0, 0.0 ]
bto_F0_R0_ave = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0] # ave equilib Force for each specie; Position
fOut_infoAve  = pathHome+'bto/cmbd_ave_s_F/info_ave'+str(ave_num)+'_'+str(t_step)+'tstep'
for clcI in calc_ind_ls:
    factor_ave = float(ave_num_ls[clc_ii])/float(ave_num)
    fIn_info   = pathAv_s_F_ls[clc_ii]+'/info_ave'+str(ave_num_ls[clc_ii])+'_'+str(t_step)+'tstep'
    with open(fIn_info) as ioIn_info:
        content      = ioIn_info.readlines()
        content      = [x.strip() for x in content]
        this_P_T_V   = [float(x) for x in content[1].split()]
        P_T_V_ave[0]+= this_P_T_V[0]*factor_ave
        P_T_V_ave[1]+= this_P_T_V[1]*factor_ave
        P_T_V_ave[2]+= this_P_T_V[2]*factor_ave
        #this_F0_R0   = [float(x) for x in content[3].split()]
    with open(fOut_infoAve,'w') as ioOut_infoAve:
        ioOut_infoAve.write('#   P   T   V\n')       
        for info in P_T_V_ave:
            ioOut_infoAve.write('   '+str(info))
        ioOut_infoAve.write('\n')





