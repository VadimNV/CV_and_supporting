# code by Vadim Nemytov (vadim.nemytov13@imperial.ac.uk)
#
# even + even  = even NEVER HAPPENS
# even + odd   = odd, odd+odd = even
# Hence find:
#            1. even terms are t2,t5,t8,... t_{2+n*3}
#            2. try expressing t8, t11 in terms of previous even terms and find a pattern
#               t_{2+n*3} = 3*t_{2+(n-1)*3} + [4*sum_{j=2,...,n} t_{2+(n-j)*3}] + 2*t1
#
# written and tested with Python 2.7.12

#t0=1   (n=-2)
t1=1   #(n=-1)
t2=2   #(n= 0)
#t5     (n= 1) t_{2+n*3}
#t8     (n= 2) t_{2+n*3} = 3*t_{2+(n-1)*3} + [4*sum_{j=2,...,n} t_{2+(n-j)*3}] + 2*t1

EvenSum   = 0
accumSum  = 0
# n=0
t_0       = 2      # t2 = t_{2+n*3} @ n=1
EvenSum  += t_0
accumSum += 0
# n=1
t_1       = 8      # t5 = t_{2+n*3} @ n=1
EvenSum  += t_1
accumSum += 4*t_0
t_nMinus1 = t_1
# n=2,...,99
for n in range(2,100) :
    t_n       = 3*t_nMinus1 + accumSum + 2*t1
    EvenSum  += t_n
    accumSum += 4*t_nMinus1
    t_nMinus1 = t_n

print 'The sum of the first 100 even numbers in the Fibonacci sequence:'
print EvenSum

#Test:
#  testSum   = 0
#  testCount = 0
#  t0=1
#  t1=1
#  for m in range(2,800) :
#      t_m = t1 + t0 # m not n
#      t0  = t1
#      t1  = t_m
#      if t_m % 2 == 0 :
#          if t_m < 200000 :
#              print t_m
#          testSum   += t_m
#          testCount += 1
#      if testCount == 100 :
#          print 'Counted to 100'
#          break
#  print testSum
