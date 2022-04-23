sum2:
params 2
param int a`2
param int b`2



~t0 = a`2 + b`2

return ~t0
#L7:
return 0

fun1:
params 4
param int n`3
param int a`3
param int b`3
param int c`3



#L15:
param n`3
param a`3
~t2 = call sum2, 2



#L17:
param b`3
param c`3
~t3 = call sum2, 2

#L13:
param ~t2
param ~t3
~t1 = call sum2, 2

return ~t1
#L11:
return 0

pp:
params 3
param char c1`4
param char c2`4
param char c3`4

output char, c1`4

#L25:
output char, c2`4

#L23:
output char, c3`4

#L21:
return 

fun2:
params 1
param int n`5

output int, n`5

#L35:
~t4 = (string) "\n"
output string, ~t4

#L33:

~t5 = 0

if n`5 == ~t5 goto #L38
goto #L37

#L38:

return
#L39:

#L37:

~t7 = 1

~t6 = n`5 - ~t7

param ~t6
call fun2, 1

#L29:
return 

start:
params 0

~t8 = 24

n`7 = (int) ~t8

#L44:

param n`7
call fun2, 1

#L42:
return 

#L41:

#L27:
#L19:
#L9:
#L5: