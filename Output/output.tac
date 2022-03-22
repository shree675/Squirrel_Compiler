start:

b = (int) 0
L8:
c = (int) 0
L6:
d = (int) 0
L4:

if c == 0 goto L13
t2 = 0
goto L12
L13:
t2 = 1
L12:
if b == 0 goto L15
if t2 == 0 goto L15
t1 = 1
goto L14
L15:
t1 = 0
L14:

t3=d >= b
if t1 != 0 goto L17
if t3 != 0 goto L17
t0 = 0
goto L16
L17:
t0 = 1
L16:

a = (int) t0

L2:

L1:
