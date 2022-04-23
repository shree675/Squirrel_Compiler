fun2:
params 1
param int n`2

output int, n`2

#L8:

~t0 = 0

if n`2 == ~t0 goto #L11
goto #L10

#L11:

return
#L12:

#L10:

~t2 = 1

~t1 = n`2 - ~t2

param ~t1
call fun2, 1

#L4:
return 

start:
params 0

~t3 = 10

n`4 = (int) ~t3

#L17:

param n`4
call fun2, 1

#L15:
return 

#L14:

#L2: