from scipy.optimize import minimize
import math
import subprocess
import os
from unitCellMaker_scale import makeScaledCell, makeScaledCell_Th

#symmetry = 'Cubic'
#symmetry = 'R3m'
symmetry = 'GrazR3m'
progC   = 'Program_Comparison'
#trajX   = '/home/vn713/ASAP_git/asap/bin/traj.x'
trajX   = '/home/vadim/asap/bin/traj.x'
#genIn   = 'genParam_etc/gen_sc_bto_TemplateQEqTi.in'
#genIn   = 'genParam_etc/gen_sc_bto_TemplateQEqOxTi_vOx.in'
genIn   = 'genParam_etc/gen_sc_bto_TemplateQEqOxTi_vTi.in'
#genIn   = 'genParam_etc/gen_sc_bto_TemplateQEqTi_qNet0.in'
#genIn   = 'genParam_etc/gen_sc_bto_TemplateQEqTi_2GPa.in' # QEqTS but paramtz'd at Pulay ~2 or -2GPa so that R3m is stable at T=0K, P=0GPa
#genIn   = 'genParam_etc/gen_sc_bto_TemplateQEqTiqd.in'
#genIn   = 'genParam_etc/gen_sc_bto_TemplateQEqOffPolON.in'
#genIn   = 'genParam_etc/gen_sc_bto_TemplateTS-MD.in'
#genIn   = 'genParam_etc/gen_sc_bto_TemplateQEqOnPolOff.in'
#genIn   = 'genParam_etc/gen_sc_bto_TemplateQEqOffPolOff.in'
genScIn = 'genParam_etc/gen_sc_temp.in'

runTraj = trajX+" < "+genScIn

# move to working asap directory
print os.getcwd()
os.chdir("bto/")
print os.getcwd()
# point to correct starting pos and cell files
fScIn=open(genScIn,'w')
with open(genIn) as gen:
    content    = gen.readlines()
    content    = [x.strip() for x in content]
    for i,line in enumerate(content):
        if   i == 17:
            #fScIn.write('posfile RXed_cel_pos/py'+symmetry+'_scaled.pos\n')
            #fScIn.write('posfile RXed_cel_pos/py'+symmetry+'_n1_scaled.pos\n')
            fScIn.write('posfile superCelPos/py'+symmetry+'_n1_scaled.pos\n')
        elif i == 18:
            #fScIn.write('celfile RXed_cel_pos/py'+symmetry+'_ang.cel\n')
            #fScIn.write('celfile RXed_cel_pos/py'+symmetry+'_n1_bohr.cel\n')
            fScIn.write('posfile superCelPos/py'+symmetry+'_n1_bohr.cel\n')
        else        :
            fScIn.write(line+'\n')
fScIn.close()

#run traj.x at input system parameters, return Stress, Forces and Energy
userInput = 'lala'
def costFn(vec_sc_TH):
    # _| set up input Pos, Cel - based on scaling factor scl and angle TH
    scale_tot = vec_sc_TH[0]
    theta     = vec_sc_TH[1]
    print scale_tot, theta
    #    go back to the original directory:
    os.chdir("../")
    #    make a scaled cell:
    if not (symmetry=='GrazR3m'):
        celFile, posFile = makeScaledCell(scale_tot,symmetry)
    else:
        celFile, posFile = makeScaledCell_Th(scale_tot,theta,symmetry)
    #    go to directory where asap is run from
    os.chdir("bto/")
    #    re-create gen_sc_temp.in file to point to updated, scaled, posfile and celfile
    fScIn=open(genScIn,'w')
    with open(genIn) as gen:
        content    = gen.readlines()
        content    = [x.strip() for x in content]
        for i,line in enumerate(content):
            if   i == 17:
                fScIn.write('posfile RXed_cel_pos/'+posFile+'\n')
            elif i == 18:
                fScIn.write('celfile RXed_cel_pos/'+celFile+'\n')
            else        :
                fScIn.write(line+'\n')
    fScIn.close()
    # _| run traj to generate Program_Comparison file
    fileIn         = open(genScIn)
    process        = subprocess.Popen(trajX.split(), stdout=subprocess.PIPE, stdin=fileIn, shell=False)
    stdout, stderr = process.communicate()
    fileIn.close()
    with open(progC) as fOut:
        content    = fOut.readlines()
        content    = [x.strip() for x in content]
    Stress         = [[float(x) for x in content[3].split()[3:6]],
                      [float(x) for x in content[4].split()[3:6]],
                      [float(x) for x in content[5].split()[3:6]]]
    Pressure       = float(content[11].split()[2])
    print Stress
    print Pressure
    wP, wSd, wSod  = 1.0    , 1.0     , 4000010.0
    wSum           = wP + wSd + wSod + wSod
    wP, wSd, wSod  = wP/wSum, wSd/wSum, wSod/wSum
    cost = math.sqrt(wP*Pressure**2 + wSd*Stress[0][1]**2 + wSod*Stress[0][1]**2 + wSod*Stress[0][2]**2)
    return cost

# _| Minimize Pressure and stress, for optimal scaling and angle
#startGuess = (1.00012649,  0.16278127)
startGuess = (1.0000001 , 0.0424700154)
#solN = minimize(costFn,startGuess,method='L-BFGS-B',bounds=((0.99,1.1),(0.13,0.17)),options={'gtol': 1e-08, 'eps': 1.0e-6, 'maxiter': 20, 'disp': False})
#solN = minimize(costFn,startGuess,method='TNC'     ,bounds=((0.99,1.1),(0.13,0.17)),options={'gtol': 1e-08, 'eps': 1.0e-05, 'maxiter': 20, 'disp': False})
solN = minimize(costFn,startGuess,method='SLSQP'    ,bounds=((0.99,1.1),(0.13,0.17)),options={'gtol': 1e-08, 'eps': 5.0e-6, 'maxiter': 20, 'disp': False})
print solN
print 'solution:', format(solN['x'][0],'.10f'), ',', format(solN['x'][1],'.10f')

# QEqTi             posfile RXed_cel_pos/pyCubic0.993127268878scaled.pos 86302scaled.pos
# QEqTi             celfile RXed_cel_pos/pyCubic0.993127268878ang.cel    86302ang.cel

# QEqTiqd           posfile RXed_cel_pos/pyCubic0.992806816977scaled.pos
# QEqTiqd           celfile RXed_cel_pos/pyCubic0.992806816977ang.cel

# QEqOffPolOn(TS)   posfile RXed_cel_pos/pyCubic0.992845280553scaled.pos
# QEqOffPolOn(TS)   celfile RXed_cel_pos/pyCubic0.992845280553ang.cel

# QEqOnPolOff(MS-Q) posfile RXed_cel_pos/pyCubic0.995498197002scaled.pos
# QEqOnPolOff(MS-Q) posfile RXed_cel_pos/pyCubic0.995498197002ang.cel  

# QEqOffPolOff(1/r) posfile RXed_cel_pos/pyCubic0.988305644003scaled.pos
# QEqOffPolOff(1/r) celfile RXed_cel_pos/pyCubic0.988305644003ang.cel
