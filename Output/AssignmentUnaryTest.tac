foo:
params 1
param int a`2

output int, a`2

#L4:
return 

start:
params 0

~t0 = 10

a`3 = (int) ~t0

#L9:

~t1 = 0 -  a`3

param ~t1
call foo, 1

#L7:
return 

#L6:

#L2: