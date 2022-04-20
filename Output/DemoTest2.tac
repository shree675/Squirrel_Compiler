~t0 = 4

var1`1 = (int) ~t0

~tf0 = 1.2

myFloat`1 = (float) ~tf0

start:

var2`2 = (int) 0
#L4:
~t1 = (int) 20
ifFalse var1`1 == ~t1 goto #L7


~tf1 = 8.4

myFloat`1 = ~tf1

#L10:
goto #L6
#L8:
#L7:

~t3 = (int) 4
ifFalse var1`1 == ~t3 goto #L12


~t2 = 82

var2`2 = ~t2

#L17:
output int, var2`2

#L15:
goto #L6
#L13:
#L12:


b`6 = (bool) false
#L19:
goto #L6

#L6:
return 

#L1:
