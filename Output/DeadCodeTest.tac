foo:
params 1
param int x`2

~t0 = (int) 8
output int, ~t0

#L8:
~t1 = 3

return ~t1
#L6:
~t2 = (int) 2
output int, ~t2

#L4:
return 0

start:
params 0

~t4 = 4

param ~t4
~t3 = call foo, 1

f`3 = (float) ~t3

#L13:
output float, f`3

#L11:
return 

#L10:

#L2: