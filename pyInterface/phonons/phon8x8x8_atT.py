import numpy as np
import subprocess
import os
from exactQpathMaker_atT import make_exactQpath_GXMGRM
from qpointBandConstructor_atT import constructBangsGnu
import shutil

sameMD      = True
if sameMD:
    #sc = 0.25
    sc = 1.0
    #sc = 0.10
ave_num     = 2000 # 2200 # 4000 # 2730 # 1000
scNum       = 1
iPrint      = 10 # 10
#
pathWork    = 'workDir/'
pathHome    = '/home/vadim/Documents/PhD_weekly_on_GitLab/PhD_Weekly_Desktop/PhD_Thesis/final_data/atT_phonons/'
fPOSCAR     = 'POSCAR'
fPOSCAR00i  = 'POSCAR-00'
fFORCE_SETS = 'FORCE_SETS'
fBandConf   = 'band.conf'
fQPOINTS    = 'QPOINTS'
fBORN       = pathHome+'bto/kSpacePath_etc/BORN'
binPhonopy  = 'phonopy'
path_md     = '/home/vadim/workspace/ASAP_runningCode/Examples/Traj/12_bto_2018_lowT_R3m/qeqON_polON/100K/8x8x8_b/' # *** ^^^
fCell1x1x1  = '/home/vadim/workspace/ASAP_runningCode/Examples/Traj/12_bto_2018_lowT_R3m/btoQEqTi/pyGrazR3m_n1_ang_1.0004.cel'
#fCart1x1x1  = '/home/vadim/workspace/ASAP_runningCode/Examples/Traj/12_bto_2018_lowT_R3m/btoQEqTi/pyGrazR3m_n1_scaled.pos'     # TODO averaged             # *** relaxed positions of atoms for this supercell in scaled coordinates.
fCart1x1x1  = pathHome+'bto/cell1x1x1ave/QEqTS8x8x8_cmbd_bf_s4_out/ave1x1x1_scaled_round.pos'
fCellM0     = 'disp_out/s5_out/Cell_M0'                                # *** CAREFUL: in bohr. Phonopy needs Angstrom
fDISP       = 'disp_out/s5_out/DISP'                                   # ***
fGen        = 'disp_out/s5_out/gen_bto_100K_fR_Sdisp.in'               # ***
#fPosAve_s   = 'bto/ave_s_F/s_Ave'+str(ave_num)+'_'+str(iPrint)+'tstep_disp_'        # ending 1_sc_1, 2_sc_1, 3_sc_1
#fForceAve   = 'bto/ave_s_F/force_au_ave'+str(ave_num)+'_'+str(iPrint)+'tstep_disp_' # ending 1_sc_1, 2_sc_1, 3_sc_1
fPosAve_s   = 'bto/cmbd_ave_s_F/s_Ave'+str(ave_num)+'_'+str(iPrint)+'tstep_disp_'        # ending 1_sc_1, 2_sc_1, 3_sc_1
fForceAve   = 'bto/cmbd_ave_s_F/force_au_ave'+str(ave_num)+'_'+str(iPrint)+'tstep_disp_' # ending 1_sc_1, 2_sc_1, 3_sc_1
#fPosAve_s   = 'bto/all_aveSameMD_s_F/aveSameMD100_s_F_qeqOn8x8x8'+"_b_s4_"+'out/s_Ave'+str(ave_num)+'_'+str(iPrint)+'tstep_disp_'
#fForceAve   = 'bto/all_aveSameMD_s_F/aveSameMD100_s_F_qeqOn8x8x8'+"_b_s4_"+'out/force_au_ave'+str(ave_num)+'_'+str(iPrint)+'tstep_disp_' # ending 1_sc_1, 2_sc_1, 3_sc_1
#
n           = 8                                               # ^^^
natUnit     = n*n*n
nat         = natUnit*(1+1+3)
dispInd     = [1,1,513,513,1025,1025,1025,1025]               # ^^^ These indices are in DISP file. I put them there manually though (from old disp.yaml files)... this is the fastest way
dispNum     = len(dispInd)
aAll        = []                                # Cell vectors
kPath       = "BAND = 0.0 0.0 0.0  0.0 0.5 0.0  0.5 0.5 0.0  0.0 0.0 0.0  0.5 0.5 0.5  0.5 0.5 0.0" # GXMGRM
#interpltion = 'interpoltd'
interpltion = 'noninterpoltd'
#
auTOang     = 0.5291772108                      # as in ASAP
angTOau     = 1.0/auTOang
auTOev_ang  = 51.41917684                       # as in ASAP au_to_evperang = 51.41917684
#
os.chdir(pathHome)
os.chdir(pathWork)
# ACT    I.  run ASAP NVE md to get average positions and forces
#            ...assuming it's already done and files are ready

# TODO Phonopy wants POSCAR for some reason... so take a relaxed 1x1x1 structure? I don't know what Phonopy uses it for, but I am providing my own SPOSCAR-001 etc and FORCE_SETS
# ACT   II.  Prepare POSCAR (not sure what it's for. I make my own POSCAR-001, -002, -003 )
ioPOSCAR = open(fPOSCAR,'w')
ioPOSCAR.write('Ba Ti O\n')
ioPOSCAR.write('1.000000000000000\n')
# ...cell vectors are held fixed in NVE md
with open(fCell1x1x1) as ioCell:
    content = ioCell.readlines()
    content = [x.strip() for x in content]
    for lineC in content[2:]:
        # ...already in Angstrom
        ai = [float(x) for x in lineC.split()]
        ioPOSCAR.write('    '+str(ai[0])+'    '+str(ai[1])+'    '+str(ai[2])+'\n')
ioPOSCAR.write(' '+str(1)+'   '+str(1)+'   '+str(3)+'\n')
ioPOSCAR.write('Direct\n')
# ...atomic positions in scaled units
with open(fCart1x1x1) as ioCart:
    content = ioCart.readlines()
    content = [x.strip() for x in content]
    for line in content[2:]:
        strPos = ''
        for x in line.split()[1:]:
            strPos += '  '+str(x)
        ioPOSCAR.write(strPos+'\n')
ioPOSCAR.close()

# ACT  III.  Prepare POSCAR-001 etc files to use as input to Phonopy
for i in [1,2,3,4,5,6,7,8]:
    ioPOSCAR00i = open(fPOSCAR00i+str(i),'w')
    ioPOSCAR00i.write('Ba Ti O\n')
    ioPOSCAR00i.write('   1.0\n')
    # ...cell vectors are held fixed in NVE md
    with open(path_md+fCellM0) as ioCell:
        content = ioCell.readlines()
        content = [x.strip() for x in content]
        for ii,line in enumerate(content):
            if '0STEP' in line:
                for lineC in content[ii+1:]:
                    # ...convert auTOang (if cell vectors are in au)
                    ai = [float(x)*auTOang for x in lineC.split()]
                    aAll.append(np.asarray(ai))
                    ioPOSCAR00i.write('    '+str(ai[0])+'    '+str(ai[1])+'    '+str(ai[2])+'\n')
    # ...number of each specie
    ioPOSCAR00i.write(' '+str(natUnit)+'   '+str(natUnit)+'   '+str(natUnit*3)+'\n')
    ioPOSCAR00i.write('Direct\n')
    # ...atomic positions in scaled units
    with open(pathHome+fPosAve_s+str(i)+'_sc_'+str(scNum)) as ioPosAve_s:
        content = ioPosAve_s.readlines()
        content = [x.strip() for x in content]
        for line in content:
            strPos = ''
            for x in line.split():
                strPos += '  '+str(x)
            ioPOSCAR00i.write(strPos+'\n')
    ioPOSCAR00i.close()

# ACT   VI.  Prepare FORCE_SETS files. Use averaged forces from ASAP md
ioFORCE_SETS = open(fFORCE_SETS,'w')
ioFORCE_SETS.write(str(nat)+'\n')
ioFORCE_SETS.write(str(dispNum)+'\n')
with open(path_md+fDISP) as ioDISP:
    content = ioDISP.readlines()
    content = [x.strip() for x in content]
    for j,line in enumerate(content):
        i=j+1
        # ...index of the displaced atom
        disp_i   = int(line.split()[0])
        ioFORCE_SETS.write('\n   '+str(disp_i)+'\n')
        # ...displacement vector in Angstrom
        with open(path_md+fGen) as ioGen:
            ccontent = ioGen.readlines()
            ccontent = [x.strip() for x in ccontent]
            for lI,lline in enumerate(ccontent):
                if 'displacement' in lline.split():
                    # ...magnitude of displacement in bohr (so convert).
                    dtf = float(lline.split()[1].replace('d0',''))*auTOang
                if 'disp_scale' in lline.split():
                    # ...magnitude of displacement in bohr (so convert).
                    #dtf = float(lline.split()[1].replace('d0',''))*auTOang
                    dtf = float(ccontent[lI+1].split()[scNum-1])*dtf       # NEW for scale .neq. 1.0, but e.g. 0.5, 0.1
            if sameMD :                                                    # Even NEWer - sameMD, sc set by hand (not in gen_bto.in )
                dtf = dtf*sc
               
        disp_v_s = [float(x) for x in line.split()[1:]]
        disp_v_r = aAll[0]*disp_v_s[0] + aAll[1]*disp_v_s[1] + aAll[2]*disp_v_s[2]
        disp_v_r = dtf*disp_v_r/np.linalg.norm(disp_v_r)
        ioFORCE_SETS.write('    '+str(disp_v_r[0])+'    '+str(disp_v_r[1])+'    '+str(disp_v_r[2])+'\n')
        # ...list of averaged forces for each atom
        with open(pathHome+fForceAve+str(i)+'_sc_'+str(scNum)) as ioForceAve:
            ccontent = ioForceAve.readlines()
            ccontent = [x.strip() for x in ccontent]
            for lline in ccontent:
                # ...Phonopy wants ev/Ang and ASAP file gives (currently) Hartree/bohr auTOev_ang
                force = [float(x)*auTOev_ang for x in lline.split()]
                ioFORCE_SETS.write('     '+str(force[0])+'    '+str(force[1])+'    '+str(force[2])+'\n')
ioFORCE_SETS.close()

# ACT  VII.  Prepare band.conf
ioBandConf = open(fBandConf,'w')
ioBandConf.write('ATOM_NAME = Ba Ti O\n')
ioBandConf.write('DIM = '+str(n)+' '+str(n)+' '+str(n)+'\n')
ioBandConf.write(kPath)
if interpltion == 'noninterpoltd':
    ioBandConf.write('\nQPOINTS = .TRUE.')
    # ...generate a set of exact q-points for this supercell (nxnxn) along GXMGRM
    make_exactQpath_GXMGRM(pathHome+pathWork+fQPOINTS,n,n,n)
ioBandConf.close()

# ACT VIII.  Calculate Phonon spectrum, connecting high symmetry points (a picture)
shutil.copyfile(fBORN,pathHome+pathWork+'BORN')
#phonopyCommand = 'phonopy -p --nac --save band.conf'  # aim to run: phonopy -p --nac --save band.conf
phonopyCommand = 'phonopy -p --save band.conf'  # aim to run: phonopy -p --nac --save band.conf
print phonopyCommand.split()
fileIn         = open(fBandConf)
process        = subprocess.Popen(phonopyCommand.split(), stdout=subprocess.PIPE, stdin=fileIn, shell=False)
stdout, stderr = process.communicate()
fileIn.close()

# ACT    X.  If calculating non-interpolated phonon spectrum then convert yaml file to gnu-plotable file
constructBangsGnu(pathHome+pathWork)
# ...now type "gnuplot < gnuPlotterThisSyst.gnu" to produce an image of bands given as pints at exact q-points

# ACT   -.   Go to "pathHome" directory
os.chdir(pathHome)





# OTHER:
#if interpltion == 'interpltd':
#    fileIn         = 'band.yaml'
#    fileOut        = 'band.gnu'
#    phonopyCommand = 'bandplot --gnuplot band.yaml > band.gnu'
#    process        = subprocess.Popen(trajX.split(), stdout=fileOut, stdin=fileIn, shell=False)
#    stdout, stderr = process.communicate()
#    fileOut.close()

