start:
params 0

n`2 = (int) 0
#L18:
~t0 = (string) "Enter a number: "
output string, ~t0

#L16:
input int, n`2

#L14:
~t1 = 1

factorial`2 = (int) ~t1

#L12:
~t2 = (string) "The factorial of "
output string, ~t2

#L10:
output int, n`2

#L8:
~t3 = (string) " is "
output string, ~t3

#L6:

~t4 = 0

if n`2 == ~t4 goto #L21
goto #L22

#L21:

~t5 = (int) 1
output int, ~t5

#L23:
goto #L20
#L22:

~t6 = 1

i`5 = (int) ~t6

#L32:


if i`5 <= n`2 goto #L33
goto #L30

#L33:




~t9 = factorial`2 * i`5

factorial`2 = ~t9

#L34:


~t7 = 1

~t8 = i`5 + ~t7

i`5 = ~t8

goto #L32
#L30:

#L29:
output int, factorial`2

#L25:

#L20:
~t10 = (string) "\n"
output string, ~t10

#L2:
return 

#L1:
