import sys

outChar = [0,1,2,3,4,5,6,7,8,9,
           'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']


def printVal_in_base(val_in,b_in) :
    # assuming that value is a number in representation base 10
    # use Euclid's quotient/remainder theorem
    # for all v,b!=0, v = q*b + r, q - quotient, r - remainder
    representation = []
    n              = 0
    q_n            = val_in
    outString      = ''
    while not q_n < b_in :
        r_n             = q_n % b_in       # the remainder
        q_n             = (q_n - r_n)/b_in # the quotient
        representation += [r_n]                  # to TEST
        n              += 1
        outString       = str(outChar[r_n]) + outString
    q_n
    representation += [q_n]                      # to TEST
    outString       = str(outChar[q_n]) + outString
    # now print
    print val_in,'to the base',b_in,' is:',outString
    #out = []
    L   = len(representation)
    testVal = 0                                  # to TEST
    for l in range(0,L) :
        charNum = representation[L-1-l]
        testVal+= charNum*b_in**(L-1-l)          # to TEST
    if val_in == testVal :                       # to TEST
        print 'test_val == val_in --> Success!'  # to TEST

printVal_in_base(464,10)                         # to TEST
printVal_in_base(465,36)                         # to TEST
