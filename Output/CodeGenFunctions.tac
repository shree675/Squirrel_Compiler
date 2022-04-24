pp:
params 3
param char c1`2
param char c2`2
param char c3`2

output char, c1`2

#L8:
output char, c2`2

#L6:
output char, c3`2

#L4:
return 

start:
params 0

char cc`3[3]
cc`3[0] = 'a'
cc`3[1] = 'b'
cc`3[2] = 'c'

#L13:
~t0 = 0

~t1 = ~t0 * 1

~t2 = ~t1 * 1
~t3 = cc`3[~t2]

~t4 = 1

~t5 = ~t4 * 1

~t6 = ~t5 * 1
~t7 = cc`3[~t6]

~t8 = 2

~t9 = ~t8 * 1

~t10 = ~t9 * 1
~t11 = cc`3[~t10]

#L17:
#L15:
param ~t3
param ~t7
param ~t11
call pp, 3

#L11:
return 

#L10:

#L2: