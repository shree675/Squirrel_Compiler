start:

~t0 = 5

a`2 = (int) ~t0

#L6:
~t1 = (bool) a`2

b`2 = (bool) ~t1

#L4:
~t2 = 0

if b`2 != ~t2 goto #L9
goto #L8
#L9:

~t3 = 0
~t4 = 1
if b`2 == ~t3 goto #L12
output int, ~t4
goto #L13
#L12:
output int, ~t3
#L13:

#L10:

#L8:
return 

#L1:
