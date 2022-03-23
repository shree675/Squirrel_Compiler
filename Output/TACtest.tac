start:

a = (int) 0
L10:
b = (int) 0
L8:
c = (int) 0
L6:
d = (int) 0
L4:
goto L15
L15:
goto L16
L16:
goto L14
L13:

i = (int) 0
L17:
goto L12
L14:

if a >= b goto L21
goto L20

L21:

if c != d goto L19
goto L20

L19:

t0 = a + b

if t0 == c goto L29
goto L28

L29:

ab = (int) 0
L30:

L28:
j = (int) 0
L24:

t1 = a + b

t2 = t1 + c

j = t2

L22:
goto L12
L20:
goto L32
L34:
goto L33
L32:

k = (int) 0
L37:

t3 = b * c

t4 = a + t3

k = t4

L35:
goto L12
L33:

x = (int) 0
L41:

t7 = - a

t8 = b + c

t6 = t7 / t8

t5 = t6 % d

x = t5

L39:

L12:
return 0

L1:
