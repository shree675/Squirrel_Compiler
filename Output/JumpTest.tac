start:

x`2 = (int) 0
#L8:
y`2 = (int) 0
#L6:
#L10:

if x`2 < 5 goto #L11
goto #L4

#L11:

j`3 = (int) 0
#L14:

if j`3 == 0 goto #L17
goto #L18

#L17:

j`3 = 1

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

~t0 = x`2 * y`2

~t1 = x`2 + ~t0

~t3 = x`2 + y`2

~t2 = y`2 * ~t3

~t4 = ~t1 + ~t2

return ~t4
#L2:
return 0

#L1:
