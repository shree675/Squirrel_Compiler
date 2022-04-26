start:
params 0

~t0 = 42

a`2 = (int) ~t0

#L12:
~t1 = 23

b`2 = (int) ~t1

#L10:
~t2 = 12

c`2 = (int) ~t2

#L8:
~t3 = 11

d`2 = (int) ~t3

#L6:
~t4 = 0

i`3 = (int) ~t4

#L17:

~t5 = 2

if i`3 < ~t5 goto #L18
goto #L15

#L18:

~t8 = 0

j`4 = (int) ~t8

#L24:

~t9 = 10

if j`4 < ~t9 goto #L25
goto #L22

#L25:

output int, j`4

#L26:


~t10 = 1

~t11 = j`4 + ~t10

j`4 = ~t11

goto #L24
#L22:

#L21:


~t6 = 1

~t7 = i`3 + ~t6

i`3 = ~t7

goto #L17
#L15:

#L14:
~t12 = (string) "\n"
output string, ~t12

#L2:
return 

#L1:
