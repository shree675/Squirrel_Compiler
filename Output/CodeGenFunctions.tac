fun1:

~t0 = 0

if n`2 == ~t0 goto #L11
goto #L10

#L11:

return
#L12:

#L10:

~t3 = 1

~t2 = n`2 - ~t3

param ~t2
~t1 = call fun1, 1

#L6:
return
#L4:
return 

start:

~t4 = 10

a`4 = (int) ~t4

#L17:

param a`4
~t5 = call fun1, 1

#L15:
return 

#L14:

#L2: