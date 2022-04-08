start:

int fibonacci`2[24]
fibonacci`2[0]=0
fibonacci`2[4]=0
fibonacci`2[8]=0
fibonacci`2[12]=0
fibonacci`2[16]=0
fibonacci`2[20]=0

#L6:

~t0 = 1 * 1

~t1 = ~t0 * 4

~t2 = (int) 1
fibonacci`2[~t1] = ~t2

#L4:

i`3 = (int) 2

#L11:

if i`3 < 6 goto #L12
goto #L9

#L12:

~t4 = i`3 * 1

~t5 = ~t4 * 4

~t6 = i`3 - 1

~t7 = ~t6 * 1

~t8 = ~t7 * 4

~t9 = i`3 - 2

~t10 = ~t9 * 1

~t11 = ~t10 * 4

~t12 = fibonacci`2[~t8] + fibonacci`2[~t11]

~t13 = (int) ~t12
fibonacci`2[~t5] = ~t13

#L15:

~t14 = i`3 * 1

~t15 = ~t14 * 4
output int, fibonacci`2[~t15]

#L13:

~t3 = i`3 + 1

i`3 = ~t3

goto #L11
#L9:

#L8:
return 

#L1:
