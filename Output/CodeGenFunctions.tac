fun1:
params 4
param int n`2
param int a`2
param int b`2
param int c`2

~t0 = 3

r`2 = (int) ~t0

#L6:

return r`2
#L4:
return 0

start:
params 0

~t1 = 10

n`3 = (int) ~t1

#L19:
~t2 = 1

a`3 = (int) ~t2

#L17:
~t3 = 2

b`3 = (int) ~t3

#L15:
~t4 = 3

c`3 = (int) ~t4

#L13:





#L25:
#L23:
#L21:
param n`3
param a`3
param b`3
param c`3
~t5 = call fun1, 4

n`3 = ~t5

#L11:
output int, n`3

#L9:
return 

#L8:

#L2: