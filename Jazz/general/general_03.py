# code by Vadim Nemytov (vadim.nemytov13@imperial.ac.uk)
#
# build output list in 'chunks', a chunk starts and ends with numbers that are greater
# than the "tail" (last number) of the previous chunk. Once a chunk is added, swap lists
# and apply the same procedure to identify the next chunk, etc. until complete. Terminate
# when all the elements of one of the lists has been verified. I think it's an O(n) method
#
# written and tested with Python 2.7.12
def f_merge_sorted(v1,v2):
    vOUT = []
    ind1 = 0
    ind2 = 0
    tReachedEnd = False
    if v1[0] < v2[0] :
        l1 = v1
        l2 = v2
    else             :
        l1 = v2
        l2 = v1
    while ind1 < len(l1):
        ind_from = ind1
        while l1[ind1] < l2[ind2] :
            ind1 += 1
            if ind1 == len(l1) :
                tReachedEnd = True
                break
        ind_to   = ind1
        vOUT = vOUT + l1[ind_from:ind_to]
        if tReachedEnd :
            #                IND2
            vOUT = vOUT + l2[ind2:]
            break
        #swap two lists and indices
        l_temp   = l1
        ind_temp = ind1
        l1       = l2
        ind1     = ind2
        l2       = l_temp
        ind2     = ind_temp
    return vOUT
