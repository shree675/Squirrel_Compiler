start:

~t0 = 25

a`2 = (int) ~t0

#L6:

b`2 = (bool) false

#L4:
~t1 = 0

if b`2 != ~t1 goto #L9
goto #L10
#L9:

output int, a`2

#L11:
goto #L8
#L10:

~t2 = 0
~t3 = 1
if b`2 == ~t2 goto #L15
output int, ~t3
goto #L16
#L15:
output int, ~t2
#L16:

#L13:

#L8:
return 

#L1:
