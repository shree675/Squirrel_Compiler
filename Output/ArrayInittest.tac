start:

int arr`2[24]
arr`2[0] = 1
arr`2[4] = 2
arr`2[8] = 12
arr`2[12] = 5
arr`2[16] = 6
arr`2[20] = 7

#L16:
char charArray`2[5]
charArray`2[0] = 'a'
charArray`2[1] = 'b'
charArray`2[2] = 'c'
charArray`2[3] = 'd'
charArray`2[4] = 'e'

#L14:
bool boolArray`2[2]
boolArray`2[0] = true
boolArray`2[1] = false

#L12:
float floatArray`2[24]
floatArray`2[0] = 1.1
floatArray`2[4] = 2.2
floatArray`2[8] = 3.3
floatArray`2[12] = 1.1
floatArray`2[16] = 2.2
floatArray`2[20] = 3.3

#L10:
int specialArray`2[48]
specialArray`2[0] = 1
specialArray`2[4] = 2
specialArray`2[8] = 3
specialArray`2[12] = 4
specialArray`2[16] = 5
specialArray`2[20] = 6
specialArray`2[24] = 1
specialArray`2[28] = 2
specialArray`2[32] = 3
specialArray`2[36] = 4
specialArray`2[40] = 5
specialArray`2[44] = 6

#L8:
char specialArrayChar`2[2]
specialArrayChar`2[0] = 'a'
specialArrayChar`2[1] = 'b'

#L6:
~t0 = 2

~t1 = ~t0 * 2
~t2 = 0
~t3 = ~t2 * 1
~t4 = ~t1 + ~t3
~t5 = 0
~t6 = ~t5 * 1
~t7 = ~t4 + ~t6

~t8 = ~t7 * 4

~t9 = 1

~t10 = ~t9 * 2
~t11 = 0
~t12 = ~t11 * 1
~t13 = ~t10 + ~t12
~t14 = 0
~t15 = ~t14 * 1
~t16 = ~t13 + ~t15

~t17 = ~t16 * 4

~t18 = 0

~t19 = ~t18 * 2
~t20 = 0
~t21 = ~t20 * 1
~t22 = ~t19 + ~t21
~t23 = 0
~t24 = ~t23 * 1
~t25 = ~t22 + ~t24

~t26 = ~t25 * 4

~tf0 = floatArray`2[~t17] + floatArray`2[~t26]

~tf1 = (float) ~tf0
floatArray`2[~t8] = ~tf1

#L4:
~t27 = 2

~t28 = ~t27 * 2
~t29 = 0
~t30 = ~t29 * 1
~t31 = ~t28 + ~t30
~t32 = 0
~t33 = ~t32 * 1
~t34 = ~t31 + ~t33

~t35 = ~t34 * 4
output float, floatArray`2[~t35]

#L2:
return 

#L1:
