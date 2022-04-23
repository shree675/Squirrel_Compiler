start:
params 0

~tf0 = 2.5

a`2 = (int) ~tf0

#L22:
output int, a`2

#L20:
~t0 = (string) "\n"
output string, ~t0

#L18:
~tf1 = 110.345

c`2 = (char) ~tf1

#L16:
output char, c`2

#L14:
~t1 = (string) "\n"
output string, ~t1

#L12:
~tf2 = 32.21

b`2 = (bool) ~tf2

#L10:
~t2 = 0
~t3 = 1
if b`2 == ~t2 goto #L24
output int, ~t3
goto #L25
#L24:
output int, ~t2
#L25:

#L8:
~t4 = (string) "\n"
output string, ~t4

#L6:
~t5 = 0

if b`2 != ~t5 goto #L27
goto #L28
#L27:

~t6 = 1


~t8 = (int) c`2
~t7 = ~t6 + ~t8

c`3 = (char) ~t7

#L31:
output char, c`3

#L29:
goto #L26
#L28:

~t9 = 0
~t10 = 1
if b`2 == ~t9 goto #L35
output int, ~t10
goto #L36
#L35:
output int, ~t9
#L36:

#L33:

#L26:
~t11 = (string) "\n"
output string, ~t11

#L2:
return 

#L1:
