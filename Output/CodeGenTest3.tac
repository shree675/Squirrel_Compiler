start:

int arr`2[16]
arr`2[0] = 0
arr`2[4] = 0
arr`2[8] = 0
arr`2[12] = 0

#L8:
~t0 = 1

sum`2 = (int) ~t0

#L6:
~t1 = 1

i`3 = (int) ~t1

#L13:

~t2 = 4

if i`3 <= ~t2 goto #L14
goto #L11

#L14:

~t5 = sum`2 * i`3

sum`2 = ~t5

#L17:
output int, i`3

#L15:

~t3 = 1

~t4 = i`3 + ~t3

i`3 = ~t4

goto #L13
#L11:

#L10:
output int, sum`2

#L2:
return 

#L1:
