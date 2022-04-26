sum:
params 2
param int a`2
param int b`2



~t0 = a`2 + b`2

return ~t0
#L4:
return 0

start:
params 0

~t1 = 1

a`3 = (int) ~t1

#L15:
~t2 = 12

b`3 = (int) ~t2

#L13:
~t3 = 133

c`3 = (int) ~t3

#L11:




#L17:
param a`3
param b`3
~t4 = call sum, 2

~t5 = c`3 + ~t4

c`3 = ~t5

#L9:
output int, c`3

#L7:
return 

#L6:

#L2: