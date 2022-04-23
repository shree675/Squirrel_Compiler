fun2:
params 1
param int n`2

output int, n`2

#L10:

~t0 = 0

if n`2 == ~t0 goto #L13
goto #L12

#L13:

return
#L14:

#L12:

~t2 = 1

~t1 = n`2 - ~t2

param ~t1
call fun2, 1

#L6:
return
#L4:
return 

start:
params 0

~t3 = 10

n`4 = (int) ~t3

#L19:

param n`4
call fun2, 1

#L17:
return 

#L16:

#L2: