start:

x`2 = (int) 0
#L12:
y`2 = (int) 0
#L10:
j`2 = (int) 0
#L8:
#L14:

~t0 = 5

if x`2 < ~t0 goto #L15
goto #L6

#L15:


~t1 = 0

if j`2 == ~t1 goto #L19
goto #L20

#L19:


~t2 = 1
~tf0 = (float) ~t2

~t3 = (int) ~tf0
j`2 = ~t3

#L23:
goto #L6
#L21:
goto #L18
#L20:



~t4 = 1

~t5 = x`2 + ~t4

x`2 = ~t5

#L25:

#L18:
goto #L14
#L6:
output int, x`2

#L4:



~t6 = x`2 * y`2

~t7 = x`2 + ~t6




~t9 = x`2 + y`2

~t8 = y`2 * ~t9

~t10 = ~t7 + ~t8

return ~t10
#L2:
return 0

#L1:
