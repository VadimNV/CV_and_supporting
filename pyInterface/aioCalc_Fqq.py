import os
import subprocess

inPreName  = 'BaTiO3rhombR3m_3x3x3_' # e.g. 300K_St8_centres.xyz
outPreName = 'bto_3x3x3_'
inPath     = 'bto/paramToProgC/MLWFs_out/'
outPath    = 'bto/paramToProgC/MLWFs_out/mlwfTOasap/input_bto_Zonly/'
#
asapInPreName = 'bto_3x3x3_'           # e.g. 300K_St8_centres.pos (angstrom), 300K_St8_centres.cel (bohr)
asapInPath    = 'bto/paramToProgC/MLWFs_out/mlwfTOasap/input_bto_Zonly/'
workDir       = 'bto/paramToProgC/MLWFs_out/mlwfTOasap/'
gen_template  = 'genFqqZonly_TT_template.in'
gen_Tk_i      = 'gen_Tk_i.in'
param_template= 'paramPTetc_5485m2_Fqq_Zonly_TT_template'
param_sp2     = 'paramPTetc_5485m2_Fqq_Zonly_TT_sp2'
#trajX         = '/home/vn713/ASAP_git/asap/bin/traj.x' # '/home/vadim/asap/bin/traj.x'
trajX         = '/home/vadim/asap/bin/traj.x'
phi_i_q_dir   = 'fort707dir_phi_i_qZonly/'
#phi_PreName   = 'fort_'     # e.g. 300K_St5.707
#force_PreName = 'force_au_' # e.g. 300K_St5
#startEndDir   = '/home/vn713/workspace/PhD_weekly_on_GitLab/PhD_Weekly_Desktop/PhD_Thesis/final_data/hist/' # '/home/vadim/Documents/PhD_weekly_on_GitLab/PhD_Weekly_Desktop/PhD_Thesis/final_data/hist/'
startEndDir   = '/home/vadim/Documents/PhD_weekly_on_GitLab/PhD_Weekly_Desktop/PhD_Thesis/final_data/hist/'
#
natUnit       = 27
spInd         = ['Ba' for i in range(0,natUnit  )]
spInd        += ['Ti' for i in range(0,natUnit  )]
spInd        += ['Ox' for i in range(0,natUnit*3)]
charges       = [ 2.0 for i in range(0,natUnit  )]
charges      += [ 4.0 for i in range(0,natUnit  )]
charges      += [-2.0 for i in range(0,natUnit*3)]
#
T  =   ['100', '200', '300', '500', '1000']
St =   [ [1,2,3,4,5,6,7,8,9,10],
         [1,2,3,4,5,6,7,8,9,10],
         [1,2,3,4,5,6,7,8,9,10],
         [1,2,3,4,5,6,7,8,9,10],
         [1,2,3,4,5,6,7,8,9,10] ]
sp2_set = ['0240','0500','0769','1000','1272']
sp2_bTT = [5.91749811067, 4.09898904924, 3.30502820589, 2.89842295273, 2.56970640187 ]
#
def sedPy(wordOld,wordNew, fileIn, fileOut_w):
    # fileOut_w must be open with 'w' option
    content = fileIn.readlines()
    content = [x.strip() for x in content]
    for line in content:
        if wordOld in line.split():
            for word in line.split():
                if not (word == wordOld):
                    fileOut_w.write('  '+word)
                else                    :
                    fileOut_w.write('  '+wordNew)
            fileOut_w.write('\n')
        else                      :
            for word in line.split():
                fileOut_w.write('  '+word)
            fileOut_w.write('\n')       
#
for bTT,sp2_str in zip(sp2_bTT,sp2_set):
    with open(workDir+param_template) as paramIn, open(workDir+param_sp2,'w') as paramOut_w:
        sedPy('c.CCCCCCCCCCE+00',str(bTT)+'E+00',paramIn,paramOut_w)
    ene_ftot_info = [[ [0.0,0.0,0.0] for I in St[Tk]] for Tk,Temp in enumerate(T)]
    for Tk,Temp in enumerate(T):
        for iI,I in enumerate(St[Tk]):
            inMLWF       = inPath  + inPreName  + Temp+'K_St'+str(I)+'_centres.xyz'
            inSCF        = inPath  + inPreName  + Temp+'K_St'+str(I)+'.scf.in'
            inMLWFind    = inPath  + inPreName  + Temp+'K_St'+str(I)+'_anchoredMLWFind.txt'
            Force_Tk_StI = []
            # _| prepare ASAP cel input file based on .scf.in (assuming bohr) |_
            outCel       = outPath + outPreName + Temp+'K_St'+str(I)+'_Zonly.cel'
            fCel         = open(outCel,'w')
            # ...assuming bohr
            fCel.write("\n")
            with open(inSCF) as fileSCF:
                content = fileSCF.readlines()
                content = [x.strip() for x in content]
                for i_SCF,line_SCF in enumerate(content):
                    if 'CELL_PARAMETERS' in line_SCF.split():
                        for ii_C in [1,2,3]:
                            ai = [float(x) for x in content[i_SCF + ii_C].split()]
                            for p in ai:
                                fCel.write("\t%s" % p)
                            fCel.write('\n')
            fCel.close()
            # _| prepare ASAP pos input file based on _centres.xyz (these are in Angstrom) |_
            # simple: take care positions and assign nominal charges
            outPos = outPath + outPreName + Temp+'K_St'+str(I)+'_Zonly.pos'
            fPos = open(outPos,'w')
            fPos.write('angstrom'+'\n')
            fPos.write("\n")
            with open(inMLWF) as fileMLWF:
                content = fileMLWF.readlines()
                content = [x.strip() for x in content]
                # ...first line is num of MLWFs+atoms
                # ...second line is comments. atoms start at line 542
                for ii_AtmPos,line_AtmPos in enumerate(content[542:]):
                   sp_pos = str(line_AtmPos.split()[0])
                   for word in line_AtmPos.split()[1:]:
                       sp_pos += '    '+str(word)
                   sp_pos +='\n'
                   fPos.write(sp_pos)
            fPos.close()
            # _| with ASAP do Program_Comparison, save force and E.S. potential of every atom
            # ...write gen.in file for this temperature and St
            fGen_Tk_i = open(workDir+gen_Tk_i,'w')
            with open(workDir+gen_template) as fileGenTemplate:
                content = fileGenTemplate.readlines()
                content = [x.strip() for x in content]
                for line_Gen in content:
                    if   'posfile'   in line_Gen.split():
                        strPos = ' posfile input_bto_Zonly/bto_3x3x3_'+str(Temp)+'K_St'+str(I)+'_Zonly.pos'+'\n'
                        fGen_Tk_i.write(strPos)
                    elif 'celfile'   in line_Gen.split():
                        strCel = ' celfile input_bto_Zonly/bto_3x3x3_'+str(Temp)+'K_St'+str(I)+'_Zonly.cel'+'\n'
                        fGen_Tk_i.write(strCel)
                    elif 'paramfile' in line_Gen.split():
                        strParam = ' paramfile paramPTetc_5485m2_Fqq_Zonly_TT_sp2\n'
                        fGen_Tk_i.write(strParam)
                    else                              :
                        strSame = ' '
                        for word in line_Gen.split():
                            strSame += str(word)+' '
                        fGen_Tk_i.write(strSame+'\n')
            fGen_Tk_i.close()
            # ...now run traj.x using this gen.in file as input
            # ...extract for every atom: force - from Program_Comparison file, E-S. potential - from fort.707
            os.chdir(workDir)
            fileIn         = open(gen_Tk_i)
            process        = subprocess.Popen(trajX.split(), stdout=subprocess.PIPE, stdin=fileIn, shell=False)
            stdout, stderr = process.communicate()
            fileIn.close()
            print phi_i_q_dir+"sp2_"+sp2_str+"/fort_"+str(Temp)+"K_St"+str(I)+"_Zonly.707"
            os.rename("fort.707", phi_i_q_dir+"sp2_"+sp2_str+"/fort_"+str(Temp)+"K_St"+str(I)+"_Zonly.707")
            with open('Program_Comparison') as fileProgC:
                content = fileProgC.readlines()
                content = [x.strip() for x in content]
                for ii_F,line_F in enumerate(content):
                    if ('Forces' in line_F.split()) and ('[Hartree/Bohr]' in line_F.split()):
                        forceAtm = [  l.split() for l in content[ii_F+1 : ii_F+1 + 135]  ]
                        for force in forceAtm:
                            Force_Tk_StI.append([  float(x) for x in force[-3:]  ])
            os.chdir(startEndDir)
            # check total energy and net force. Save to file Tk,StI
            for_tot = [0.0,0.0,0.0]
            fForce_Tk_i = open(workDir+phi_i_q_dir+"sp2_"+sp2_str+"/force_au_"+Temp+'K_St'+str(I)       ,'w')
            for j, f_i in enumerate(Force_Tk_StI):
                for jj,fx in enumerate(f_i):
                    for_tot[jj] += fx
                fForce_Tk_i.write( str(f_i[0])+'    '+str(f_i[1])+'    '+str(f_i[2])+'\n' )
            fForce_Tk_i.close()
            print Temp,I,'f_tot:',for_tot
            ene_ftot_info[Tk][iI][0:] = for_tot
            #
    fInfo = open(workDir+phi_i_q_dir+'info_ene_ftot.txt','w')
    fInfo.write('# T, St_i, ene_tot(n/a), force_tot \n')
    for Tk,Temp in enumerate(T):
        for iI,I in enumerate(St[Tk]):
            fInfo.write(Temp+'    '+str(I))
            for info_ii in ene_ftot_info[Tk][iI]:
                fInfo.write('    '+str(info_ii))
            fInfo.write('\n')
    fInfo.close()
