start:

a`2 = (int) 0
#L16:
b`2 = (int) 0
#L14:
c`2 = (int) 0
#L12:
d`2 = (int) 0
#L10:

ab`2 = (char) 'a'

#L8:

bc`2 = (char) 'b'

#L6:

~t1 = (int) ab`2
~t0 = ~t1 + bc`2

de`2 = (char) ~t0

#L4:
goto #L21
#L21:
goto #L22
#L22:
goto #L20
#L19:

i`3 = (int) 0
#L23:
goto #L18
#L20:

if a`2 >= b`2 goto #L27
goto #L26

#L27:

if c`2 != d`2 goto #L25
goto #L26

#L25:

~t2 = a`2 + b`2

if ~t2 == c`2 goto #L35
goto #L34

#L35:

ab`5 = (int) 0
#L36:

#L34:
j`4 = (int) 0
#L30:

~t3 = a`2 + b`2

~t4 = ~t3 + c`2

j`4 = ~t4

#L28:
goto #L18
#L26:
goto #L38
#L40:
goto #L39
#L38:

k`6 = (int) 0
#L43:

~t5 = b`2 * c`2

~t6 = a`2 + ~t5

k`6 = ~t6

#L41:
goto #L18
#L39:

x`7 = (int) 0
#L47:

~t9 = - a`2

~t10 = b`2 + c`2

~t8 = ~t9 / ~t10

~t7 = ~t8 % d`2

x`7 = ~t7

#L45:

#L18:
return 0

#L1:
