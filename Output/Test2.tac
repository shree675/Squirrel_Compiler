start:
params 0

n`2 = (int) 0
#L10:
~t0 = (string) "Enter a number: "
output string, ~t0

#L8:
input int, n`2

#L6:
~t1 = 1

i`2 = (int) ~t1

#L4:
#L12:


if i`2 <= n`2 goto #L13
goto #L2

#L13:

~t2 = 1

c`3 = (int) ~t2

#L22:
~t3 = 1

j`3 = (int) ~t3

#L20:
#L24:


if j`3 <= i`2 goto #L25
goto #L18

#L25:

output int, c`3

#L32:
~t4 = (string) " "
output string, ~t4

#L30:




~t7 = i`2 - j`3

~t6 = c`3 * ~t7


~t5 = ~t6 / j`3

c`3 = ~t5

#L28:


~t8 = 1

~t9 = j`3 + ~t8

j`3 = ~t9

#L26:
goto #L24
#L18:
~t10 = (string) "\n"
output string, ~t10

#L16:


~t11 = 1

~t12 = i`2 + ~t11

i`2 = ~t12

#L14:
goto #L12
#L2:
return 

#L1:
