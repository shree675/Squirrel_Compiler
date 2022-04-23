start:
params 0

float arr`2[16]
arr`2[0] = 0.0
arr`2[4] = 0.0
arr`2[8] = 0.0
arr`2[12] = 0.0

#L8:
~tf0 = 1.0

sum`2 = (float) ~tf0

#L6:
~t0 = 0

i`3 = (int) ~t0

#L13:

~t1 = 4

if i`3 < ~t1 goto #L14
goto #L11

#L14:


~t4 = i`3 * 1

~t5 = ~t4 * 4


~t6 = 1

~t7 = i`3 + ~t6
~tf1 = (float) ~t7

arr`2[~t5] = ~tf1

#L21:



~t8 = i`3 * 1

~t9 = ~t8 * 4
~tf3 = arr`2[~t9]

~tf2 = sum`2 * ~tf3

sum`2 = ~tf2

#L19:

~t10 = i`3 * 1

~t11 = ~t10 * 4
output float, arr`2[~t11]

#L17:
~t12 = (string) "\n"
output string, ~t12

#L15:


~t2 = 1

~t3 = i`3 + ~t2

i`3 = ~t3

goto #L13
#L11:

#L10:
output float, sum`2

#L2:
return 

#L1:
