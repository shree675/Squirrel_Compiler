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

~t11 = 0

i`7 = (int) ~t11

#L25:

~t12 = 10

if i`7 < ~t12 goto #L26
goto #L23

#L26:


param i`7
~t15 = call fibonacci, 1

a`7 = (int) ~t15

#L31:
output int, a`7

#L29:
~t16 = (string) "\n"
output string, ~t16

#L27:


~t13 = 1

~t14 = i`7 + ~t13

i`7 = ~t14

goto #L25
#L23:

#L22:
return 

#L19:

#L2: