import math
import numpy as np

try:
    inputSTR=str(raw_input()) #expecting three strings: path, inFile name, outFile name
    pathQpts, fileQpts, fileQout = inputSTR.split()
    #pathQpts      = 'bto/kSpacePath_etc/'
    #fileQpts      = 'QPOINTSpyGXMGRM'
    #fileQout      = 'QPOINTS'                    # careful ! might overwrite exisiting file
except ValueError:
    print "Not a string"

# https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
# https://stackoverflow.com/questions/323750/how-to-access-previous-next-element-while-for-looping
def thisNext(iterbleIn):                # take input    'iteratable' (a python built-in structure. e.g. list, string, etc, any object with for ... in ... property)
    iterator     = iter(iterbleIn[:-1]) # convert it to 'generator'. Unlike 'iteratable' this can be run once, and values are created and forgotten on the fly - not kept in memory
    next_item    = None
    current_item = next(iterator)       # throws StopIteration if empty.
    for next_item in iterator:
        yield (current_item, next_item)
        current_item = next_item
    yield (current_item, iterbleIn[-1])

qptData       = open(pathQpts+fileQpts)
content       = qptData.readlines()
content       = [x.strip() for x in content]
qNum          = 0

qFirst        = np.asarray([float(x) for x in content[1].split()[0:3]])
fOut          = open(pathQpts+fileQout,'w')
fOut.write(str(qFirst[0])+'\t'+str(qFirst[1])+'\t'+str(qFirst[2])+'\n')
qNum         += 1
for thisLine,nextLine in thisNext(content[1:]):
    qThis     = np.asarray([float(x) for x in thisLine.split()[0:3]])
    qNext     = np.asarray([float(x) for x in nextLine.split()[0:3]])
    num       = int(thisLine.split()[3])    # how many points inbetween? e.g. 10 means, 1st = qThis, 10th=qNext and add 8 inbetween at |qNext-qThis|/9 spacings
    qDiff     = qNext - qThis
    nrm       = np.linalg.norm(qDiff)
    dq        = nrm/(float(num) - 1.0)
    for i in range(1,num):
        qAdd  = qThis + (float(i)*dq/nrm)*qDiff
        fOut.write(str(qAdd[0])+'\t'+str(qAdd[1])+'\t'+str(qAdd[2])+'\n')
        qNum += 1
fOut.close()
# https://stackoverflow.com/questions/5914627/prepend-line-to-beginning-of-a-file 
line          = str(qNum)
with open(pathQpts+fileQout,'r+') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(line.rstrip('\r\n') + '\n' + content)
