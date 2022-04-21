start:

var2`2 = (int) 0
#L8:
~t0 = 20

var1`2 = (int) ~t0

#L6:
~tf0 = 1.2

myFloat`2 = (float) ~tf0

#L4:
~t1 = (int) 20
ifFalse var1`2 == ~t1 goto #L11


~tf1 = 8.4

myFloat`2 = ~tf1

#L16:
output float, myFloat`2

#L14:
goto #L10
#L12:
#L11:

~t3 = (int) 4
ifFalse var1`2 == ~t3 goto #L18


~t2 = 82

var2`2 = ~t2

#L23:
output int, var2`2

#L21:
goto #L10
#L19:
#L18:


b`6 = (bool) false
#L27:
~t4 = 0
~t5 = 1
if b`6 == ~t4 goto #L29
output int, ~t5
goto #L30
#L29:
output int, ~t4
#L30:

#L25:
goto #L10

#L10:
return 

#L1:
