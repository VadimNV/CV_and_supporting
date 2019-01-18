import math
import numpy as np

#  follows simple cubic GXMGRM
def make_exactQpath_GXMGRM(fileQout,nx,ny,nz):
    #  | method returns (this,next)  |          # https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
    # _| pairs from input list ____  |_         # https://stackoverflow.com/questions/323750/how-to-access-previous-next-element-while-for-looping
    def thisNext(iterbleIn):                    # take input    'iteratable' (a python built-in structure. e.g. list, string, etc, any object with for ... in ... property)
        iterator     = iter(iterbleIn[:-1])     # convert it to 'generator'. Unlike 'iteratable' this can be run once, and values are created and forgotten on the fly - not kept in memory
        next_item    = None
        current_item = next(iterator)           # throws StopIteration if empty.
        for next_item in iterator:
            yield (current_item, next_item)
            current_item = next_item
        yield (current_item, iterbleIn[-1])
    
    G = [0.0,0.0,0.0]
    X = [0.5,0.0,0.0]
    M = [0.5,0.5,0.0]
    R = [0.5,0.5,0.5]
    # _| build q-exact grid _______  |_
    qExact     = []
    qExactPath = []
    dqPath     = []
    for mx in range(0,int(math.floor(nx/2))+1):
        for my in range(0,int(math.floor(ny/2))+1):
            for mz in range(0,int(math.floor(nz/2))+1):
                q = [float(mx)/float(nx), float(my)/float(ny), float(mz)/float(nz)]
                qExact.append(q)
                #check if q on the GXMGRM path and not Gamma
                if not (mx==0 and my==0 and mz==0):
                    if      my==0 and mz==0             : # Gamma - X path
                        qExactPath.append(q)
                        dq = math.sqrt((q[0]-G[0])**2+(q[1]-G[1])**2+(q[2]-G[2])**2)
                        dqPath.append(dq)
                    elif 2*mx==nx and mz==0             : # X - M     path
                        qExactPath.append(q)
                        dq = math.sqrt((q[0]-X[0])**2+(q[1]-X[1])**2+(q[2]-X[2])**2)+0.5
                        dqPath.append(dq)
                    elif   mx==my and mz == 0           : # M - Gamma path
                        qExactPath.append(q)
                        dq = math.sqrt((q[0]-M[0])**2+(q[1]-M[1])**2+(q[2]-M[2])**2)+0.5+0.5
                        dqPath.append(dq)
                    elif   mx==my and my==mz and mz==mx : # Gamma - R path
                        qExactPath.append(q)
                        dq = math.sqrt((q[0]-G[0])**2+(q[1]-G[1])**2+(q[2]-G[2])**2)+0.5+0.5+math.sqrt(2.0)/2.0
                        dqPath.append(dq)
                    elif 2*mx==nx and 2*my==ny          : # R - M     path
                        qExactPath.append(q)
                        dq = math.sqrt((q[0]-R[0])**2+(q[1]-R[1])**2+(q[2]-R[2])**2)+0.5+0.5+math.sqrt(2.0)/2.0+math.sqrt(3.0)/2.0
                        dqPath.append(dq)
    
    qExactPath = [ q for dq,q in sorted(zip(dqPath,qExactPath), key=lambda pair: pair[0])]
    dqPath     = [dq for dq,q in sorted(zip(dqPath,qExactPath), key=lambda pair: pair[0])]
    
    # _| write QPOINTS ____________  |_
    fOut          = open(fileQout,'w')
    fOut.write(str(len(dqPath))+'\n')
    for q in qExactPath:
        fOut.write(str(q[0])+'\t'+str(q[1])+'\t'+str(q[2])+'\n') # exact q-point on GXMGRM path
    fOut.close()
    # _| write dq for later plotting |_
    fOut          = open(fileQout+'_toPlot','w')
    for dq in dqPath:
        fOut.write(str(dq)+'\n') # exact q-point on GXMGRM path
    fOut.close()
