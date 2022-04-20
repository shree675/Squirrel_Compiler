start:

x`2 = (int) 0
#L8:
y`2 = (int) 0
#L6:
#L10:

~t0 = 5

if x`2 < ~t0 goto #L11
goto #L4

#L11:

j`3 = (int) 0
#L14:

~t1 = 0

if j`3 == ~t1 goto #L17
goto #L18

#L17:

~t2 = 1

j`3 = ~t2

#L21:
goto #L10
#L19:
goto #L16
#L18:

goto #L4
#L23:

#L16:
goto #L10
#L4:

~t3 = x`2 * y`2

~t4 = x`2 + ~t3

~t6 = x`2 + y`2

~t5 = y`2 * ~t6

~t7 = ~t4 + ~t5

return ~t7
#L2:
return 0

#L1:
