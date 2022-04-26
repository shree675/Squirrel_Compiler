start:
params 0

~t0 = 'a'

f`2 = (float) ~t0

#L18:
output float, f`2

#L16:
~t1 = (string) "\n"
output string, ~t1

#L14:
~t2 = 'a'

b1`2 = (bool) ~t2

#L12:
~t3 = 0

b2`2 = (bool) ~t3

#L10:
~t4 = 0
~t5 = 1
if b1`2 == ~t4 goto #L20
output int, ~t5
goto #L21
#L20:
output int, ~t4
#L21:

#L8:
~t6 = (string) "\n"
output string, ~t6

#L6:
~t7 = 0
~t8 = 1
if b2`2 == ~t7 goto #L22
output int, ~t8
goto #L23
#L22:
output int, ~t7
#L23:

#L4:
~t9 = (string) "\n"
output string, ~t9

#L2:
return 

#L1:
