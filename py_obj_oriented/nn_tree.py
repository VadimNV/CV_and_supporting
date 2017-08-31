import numpy as np
from scipy import spatial

def getNNlist(filePos,fileCel,Tk,i):
    #
    T              = ['100','200','300','500','1000']
    # i+1 indexing (1,...,10). So for input i=0, convert to i=0+1
    with open(filePos+T[Tk]+"K_"+str(i+1)+".dat") as file:
        dataPos    = [[float(digit) for digit in line.split()] for line in file]
    nat            = len(dataPos)
    natUnit        = len(dataPos)/5 # = 27
    #
    dataCel  = [[0.0,0.0,0.0] for y in range(0,3)]
    map27to1 = [ 0 for y in range(0,nat*27)]
    fp = open(fileCel+T[Tk]+"K_"+str(i+1)+".cel")
    for i, line in enumerate(fp):
        if i >=2:
            dataCel[i-2] = [float(digit) for digit in line.split()]
    fp.close()
    dataCel = np.asarray(dataCel)
    #
    dataPos27 = [[0.0,0.0,0.0] for y in range(0,len(dataPos)*27)]
    dataPos27 = np.asarray(dataPos27)
    for i in range(0,len(dataPos)):
        dataPos27[i+ 1*nat]=dataPos[i] + 1.0*dataCel[0] - 1.0*dataCel[1] - 1.0*dataCel[2]
        dataPos27[i+ 2*nat]=dataPos[i] + 1.0*dataCel[0]                  - 1.0*dataCel[2]
        dataPos27[i+ 3*nat]=dataPos[i] + 1.0*dataCel[0] + 1.0*dataCel[1] - 1.0*dataCel[2]
        dataPos27[i+ 4*nat]=dataPos[i]                  - 1.0*dataCel[1] - 1.0*dataCel[2]
        dataPos27[i+ 5*nat]=dataPos[i]                                   - 1.0*dataCel[2]
        dataPos27[i+ 6*nat]=dataPos[i]                  + 1.0*dataCel[1] - 1.0*dataCel[2]
        dataPos27[i+ 7*nat]=dataPos[i] - 1.0*dataCel[0] - 1.0*dataCel[1] - 1.0*dataCel[2]
        dataPos27[i+ 8*nat]=dataPos[i] - 1.0*dataCel[0]                  - 1.0*dataCel[2]
        dataPos27[i+ 9*nat]=dataPos[i] - 1.0*dataCel[0] + 1.0*dataCel[1] - 1.0*dataCel[2]
        #
        dataPos27[i+10*nat]=dataPos[i] + 1.0*dataCel[0] - 1.0*dataCel[1]
        dataPos27[i+11*nat]=dataPos[i] + 1.0*dataCel[0]                 
        dataPos27[i+12*nat]=dataPos[i] + 1.0*dataCel[0] + 1.0*dataCel[1]
        dataPos27[i+13*nat]=dataPos[i]                  - 1.0*dataCel[1]
        dataPos27[i       ]=dataPos[i]                                  
        dataPos27[i+14*nat]=dataPos[i]                  + 1.0*dataCel[1]
        dataPos27[i+15*nat]=dataPos[i] - 1.0*dataCel[0] - 1.0*dataCel[1]
        dataPos27[i+16*nat]=dataPos[i] - 1.0*dataCel[0]                 
        dataPos27[i+17*nat]=dataPos[i] - 1.0*dataCel[0] + 1.0*dataCel[1]
        #
        dataPos27[i+18*nat]=dataPos[i] + 1.0*dataCel[0] - 1.0*dataCel[1] + 1.0*dataCel[2]
        dataPos27[i+19*nat]=dataPos[i] + 1.0*dataCel[0]                  + 1.0*dataCel[2]
        dataPos27[i+20*nat]=dataPos[i] + 1.0*dataCel[0] + 1.0*dataCel[1] + 1.0*dataCel[2]
        dataPos27[i+21*nat]=dataPos[i]                  - 1.0*dataCel[1] + 1.0*dataCel[2]
        dataPos27[i+22*nat]=dataPos[i]                                   + 1.0*dataCel[2]
        dataPos27[i+23*nat]=dataPos[i]                  + 1.0*dataCel[1] + 1.0*dataCel[2]
        dataPos27[i+24*nat]=dataPos[i] - 1.0*dataCel[0] - 1.0*dataCel[1] + 1.0*dataCel[2]
        dataPos27[i+25*nat]=dataPos[i] - 1.0*dataCel[0]                  + 1.0*dataCel[2]
        dataPos27[i+26*nat]=dataPos[i] - 1.0*dataCel[0] + 1.0*dataCel[1] + 1.0*dataCel[2]
        ##
        for j in range(0,27):
            map27to1[i+ j*nat] = i
    
    myTree = spatial.cKDTree(dataPos27,leafsize=100)
    NNindBa   = np.asarray([[0 for x in range(0,12)] for y in range(0,natUnit  )])
    NNindTi   = np.asarray([[0 for x in range(0,6 )] for y in range(0,natUnit  )])
    NNindOxTi = np.asarray([[0 for x in range(0,2 )] for y in range(0,natUnit*3)])
    NNindOxBa = np.asarray([[0 for x in range(0,4 )] for y in range(0,natUnit*3)])
    #
    NNind_NotMapD_Ba   = np.asarray([[0 for x in range(0,12)] for y in range(0,natUnit  )])
    NNind_NotMapD_Ti   = np.asarray([[0 for x in range(0,6 )] for y in range(0,natUnit  )])
    NNind_NotMapD_OxTi = np.asarray([[0 for x in range(0,2 )] for y in range(0,natUnit*3)])
    NNind_NotMapD_OxBa = np.asarray([[0 for x in range(0,4 )] for y in range(0,natUnit*3)])
    i=0
    for item in dataPos:
        if    i < 27         : # Ba
            TheResult = myTree.query(item, k=13, distance_upper_bound=7.0)
            NNindBa[            i             ] = [ map27to1[TheResult[1][j]] for j in range(1,13) ] # Ba-Ox
            NNind_NotMapD_Ba[   i             ] = [          TheResult[1][j]  for j in range(1,13) ] # Ba-Ox unMapped (to calc |Rij|)
        elif 26 < i and i < 54 : # Ti          
            TheResult = myTree.query(item, k=7 , distance_upper_bound=7.0)
            NNindTi[            i -   natUnit ] = [ map27to1[TheResult[1][j]] for j in range(1,7 ) ] # Ti-Ox
            NNind_NotMapD_Ti[   i -   natUnit ] = [          TheResult[1][j]  for j in range(1,7 ) ] # Ti-Ox unMapped (to calc |Rij|)
        else                 : # Ox
            TheResult = myTree.query(item, k=7 , distance_upper_bound=7.0)
            NNindOxTi[          i - 2*natUnit ] = [ map27to1[TheResult[1][j]] for j in range(1,3 ) ] # Ox-Ti < 4.2 (1,2)
            NNindOxBa[          i - 2*natUnit ] = [ map27to1[TheResult[1][j]] for j in range(3,7 ) ] # Ox-Ba < 5.4 (3,4,5,6)
            NNind_NotMapD_OxTi[ i - 2*natUnit ] = [          TheResult[1][j]  for j in range(1,3 ) ] # Ox-Ti < 4.2 (1,2)     unMapped (to calc |Rij|)
            NNind_NotMapD_OxBa[ i - 2*natUnit ] = [          TheResult[1][j]  for j in range(3,7 ) ] # Ox-Ba < 5.4 (3,4,5,6) unMapped (to calc |Rij|)
        i=i+1
    #
    return NNindBa, NNindTi, NNindOxTi, NNindOxBa, NNind_NotMapD_Ba, NNind_NotMapD_Ti, NNind_NotMapD_OxTi, NNind_NotMapD_OxBa, dataPos27
