start:

~t0 = 'b'

var1`2 = (char) ~t0

#L6:
~t1 = 0

var2`2 = (int) ~t1

#L4:
~t5 = (char) 'b'
ifFalse var1`2 == ~t5 goto #L9

~t3 = (int) 50
ifFalse var2`2 == ~t3 goto #L15

~t2 = 2

n`6 = (int) ~t2

#L20:
output int, n`6

#L18:
goto #L14
#L16:
#L15:


~t4 = 4

a`7 = (int) ~t4

#L24:
output int, a`7

#L22:
goto #L14

#L14:
goto #L8
#L10:
#L9:

~t9 = (char) 'a'
ifFalse var1`2 == ~t9 goto #L26

~t6 = 1

j`8 = (int) ~t6

#L33:
~t7 = 3

q`8 = (int) ~t7

#L31:


~t8 = j`8 + q`8

k`8 = (int) ~t8

#L29:
output int, k`8

#L27:
#L26:


~t10 = 12

k`9 = (int) ~t10

#L37:
output int, k`9

#L35:
goto #L8

#L8:
return 

#L1:
