fibonacci:

if n == 0 goto L16
goto L17

L17:

if n == 1 goto L16
goto L15

L16:

return n
L18:

L15:

t0 = n - 1

prev = (int) t0

L11:

t1 = n - 2

prev_prev = (int) t1

L9:

param prev
t2 = call fibonacci,1

param prev_prev
t3 = call fibonacci,1

t5 = (int) t2
t4 = t5 + t3

t = (int) t4

L7:

return t
L5:
return 0

L4:

start:

length = (int) 0
L26:
input int, length

L24:

param length
t6 = call fibonacci,1

result = (int) t6

L22:
output int, result

L20:
return 

L2: