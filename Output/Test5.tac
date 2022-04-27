start:
params 0

float arr`2[36]
arr`2[0] = 1.0
arr`2[4] = 2.0
arr`2[8] = 3.0
arr`2[12] = 4.0
arr`2[16] = 5.0
arr`2[20] = 6.0
arr`2[24] = 7.0
arr`2[28] = 8.0
arr`2[32] = 9.0

#L6:
~t0 = 0

~t1 = ~t0 * 3
~t2 = 0
~t3 = ~t2 * 1
~t4 = ~t1 + ~t3

~t5 = ~t4 * 4

~t6 = 1

~t7 = ~t6 * 3
~t8 = 1
~t9 = ~t8 * 1
~t10 = ~t7 + ~t9

~t11 = ~t10 * 4
~tf0 = arr`2[~t11]

~t12 = 2

~t13 = ~t12 * 3
~t14 = 2
~t15 = ~t14 * 1
~t16 = ~t13 + ~t15

~t17 = ~t16 * 4
~tf1 = arr`2[~t17]

~tf2 = ~tf0 + ~tf1

~tf3 = (float) ~tf2
arr`2[~t5] = ~tf3

#L4:
~t18 = 0

~t19 = ~t18 * 3
~t20 = 0
~t21 = ~t20 * 1
~t22 = ~t19 + ~t21

~t23 = ~t22 * 4
output float, arr`2[~t23]

#L2:
return 

#L1:
