fibonacci:

if n`2 == 0 goto #L9
goto #L10

#L10:

if n`2 == 1 goto #L9
goto #L8

#L9:

return n`2
#L11:

#L8:

~t1 = n`2 - 1

param ~t1
~t0 = call fibonacci,1

~t3 = n`2 - 2

param ~t3
~t2 = call fibonacci,1

~t5 = (int) ~t0
~t4 = ~t5 + ~t2

return ~t4
#L4:
return 0

start:

length`4 = (int) 0
#L20:
input int, length`4

#L18:

param length`4
~t6 = call fibonacci,1

result`4 = (int) ~t6

#L16:
output int, result`4

#L14:
return 

#L13:

#L2: