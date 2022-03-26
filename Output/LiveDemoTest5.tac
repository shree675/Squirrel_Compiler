fibonacci:

if n == 0 goto L10
goto L11

L11:

if n == 1 goto L10
goto L9

L10:

return n
L12:

L9:

t1 = n - 1

param t1
t0 = call fibonacci,1

t3 = n - 2

param t3
t2 = call fibonacci,1

t5 = (int) t0
t4 = t5 + t2

return t4
L5:
return 0

L4:

start:

length = (int) 0
L20:
input int, length

L18:

param length
t6 = call fibonacci,1

result = (int) t6

L16:
output int, result

L14:
return 

L2: