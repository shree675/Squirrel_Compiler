start:

a`2 = (int) 0
#L10:
b`2 = (int) 0
#L8:
c`2 = (int) 0
#L6:
d`2 = (int) 0
#L4:
goto #L15
#L15:
goto #L16
#L16:
goto #L14
#L13:

i`3 = (int) 0
#L17:
goto #L12
#L14:

if a`2 >= b`2 goto #L21
goto #L20

#L21:

if c`2 != d`2 goto #L19
goto #L20

#L19:

~t0 = a`2 + b`2

if ~t0 == c`2 goto #L29
goto #L28

#L29:

ab`5 = (int) 0
#L30:

#L28:
j`4 = (int) 0
#L24:

~t1 = a`2 + b`2

~t2 = ~t1 + c`2

j`4 = ~t2

#L22:
goto #L12
#L20:
goto #L32
#L34:
goto #L33
#L32:

k`6 = (int) 0
#L37:

~t3 = b`2 * c`2

~t4 = a`2 + ~t3

k`6 = ~t4

#L35:
goto #L12
#L33:

x`7 = (int) 0
#L41:

~t7 = - a`2

~t8 = b`2 + c`2

~t6 = ~t7 / ~t8

~t5 = ~t6 % d`2

x`7 = ~t5

#L39:

#L12:
return 0

#L1:
