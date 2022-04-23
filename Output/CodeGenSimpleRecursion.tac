fibonacci:
params 1
param int n`2


~t0 = 0

if n`2 == ~t0 goto #L7
goto #L8

#L7:

~t1 = 0

return ~t1
#L9:
goto #L6
#L8:

~t2 = 1

if n`2 == ~t2 goto #L11
goto #L12

#L11:

~t3 = 1

return ~t3
#L13:
goto #L6
#L12:


~t6 = 1

~t5 = n`2 - ~t6

param ~t5
~t4 = call fibonacci, 1


~t9 = 2

~t8 = n`2 - ~t9

param ~t8
~t7 = call fibonacci, 1

~t10 = ~t4 + ~t7

r`5 = (int) ~t10

#L17:

return r`5
#L15:

#L6:
return 0

start:
params 0

~t11 = 3

n`6 = (int) ~t11

#L26:

param n`6
~t12 = call fibonacci, 1

a`6 = (int) ~t12

#L24:
output int, a`6

#L22:
~t13 = (string) "\n"
output string, ~t13

#L20:
return 

#L19:

#L2: