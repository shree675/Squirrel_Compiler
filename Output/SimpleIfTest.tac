start:
params 0

~t0 = 42

a`2 = (int) ~t0

#L12:
b`2 = (int) 0
#L10:
~t1 = 51

c`2 = (int) ~t1

#L8:
~t2 = 100

d`2 = (int) ~t2

#L6:


if a`2 < b`2 goto #L15
goto #L16

#L15:

~t3 = (string) "Yes"
output string, ~t3

#L17:
goto #L14
#L16:


if c`2 < d`2 goto #L19
goto #L20

#L19:

~t4 = (string) "Maybe"
output string, ~t4

#L21:
goto #L14
#L20:

~t5 = (string) "No"
output string, ~t5

#L23:

#L14:
~t6 = (string) "\n"
output string, ~t6

#L2:
return 

#L1:
