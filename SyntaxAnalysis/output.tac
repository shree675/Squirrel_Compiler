start:

int x = 0
L9:

int y = 0
L7:

L11:


t0 = x * y

if t0 != 0 goto L12
goto L5
L12:



t1 = x + 1

x = t1
L17:



t2 = y + 1

y = t2
L15:

int a = 0
L13:

goto L11
L5:

int i = 0
L22:


t3 = x - y

if t3 != 0 goto L23
goto L20
L23:

int j = 0
L24:



t4 = i + x

i = t4
goto L22
L20:

L20:

L19:


L2:
