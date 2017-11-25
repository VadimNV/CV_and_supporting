#Vadim Nemytov (vadim.nemytov13@imperial.ac.uk)
#Jazz Networks Python Test problem 3

def SqrEven(lst):
    sumOut = 0
    for a in lst :
        if a % 2 == 0 :
            sumOut += a*a
    return sumOut
