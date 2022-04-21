start:

~t0 = 'a'

x`2 = (char) ~t0

#L12:
~tf0 = 2.0

a`2 = (float) ~tf0

#L10:
~tf1 = 3.0

b`2 = (float) ~tf1

#L8:
~t1 = 0

c`2 = (int) ~t1

#L6:


~t4 = (int) a`2
~t5 = (int) b`2
~t6 = 0
if ~t4 == ~t6 goto #L17
if ~t5 == ~t6 goto #L17
~t3 = true
goto #L16
#L17:
~t3 = false
#L16:


~t7 = (int) ~t3
~t8 = 0
if ~t7 != ~t8 goto #L19
if c`2 != ~t8 goto #L19
~t2 = false
goto #L18
#L19:
~t2 = true
#L18:

~t9 = (char) ~t2
x`2 = ~t9

#L4:
output char, x`2

#L2:
return 

#L1:
