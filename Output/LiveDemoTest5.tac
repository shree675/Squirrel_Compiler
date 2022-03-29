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

t|1 = n - 1

param t|1
t|0 = call fibonacci,1

t|3 = n - 2

param t|3
t|2 = call fibonacci,1

t|5 = (int) t|0
t|4 = t|5 + t|2

return t|4
L5:
return 0

L4:

start:

length = (int) 0
L20:
input int, length

L18:

param length
t|6 = call fibonacci,1

result = (int) t|6

L16:
output int, result

L14:
return 

L2: