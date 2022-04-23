start:
params 0

int arr`2[24]
arr`2[0] = 1
arr`2[4] = 2
arr`2[8] = 12
arr`2[12] = 5
arr`2[16] = 6
arr`2[20] = 7

#L10:
~t0 = 2

i`2 = (int) ~t0

#L8:
~t1 = 0

j`2 = (int) ~t1

#L6:
~t2 = 0

~t3 = ~t2 * 2
~t4 = 1
~t5 = ~t4 * 1
~t6 = ~t3 + ~t5

~t7 = ~t6 * 4


~t9 = i`2 * 2
~t10 = j`2 * 1
~t11 = ~t9 + ~t10

~t12 = ~t11 * 4
~t13 = arr`2[~t12]

~t14 = 2

~t8 = ~t13 * ~t14

~t15 = (int) ~t8
arr`2[~t7] = ~t15

#L4:
~t16 = 0

~t17 = ~t16 * 2
~t18 = 1
~t19 = ~t18 * 1
~t20 = ~t17 + ~t19

~t21 = ~t20 * 4
output int, arr`2[~t21]

#L2:
return 

#L1:
