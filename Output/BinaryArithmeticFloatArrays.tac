start:

float myArray`2[20]
myArray`2[0] = 1.1
myArray`2[4] = 2.2
myArray`2[8] = 3.3
myArray`2[12] = 4.4
myArray`2[16] = 5.5

#L8:
~t0 = 1

~t1 = ~t0 * 1

~t2 = ~t1 * 4

~t3 = 4

~t4 = ~t3 * 1

~t5 = ~t4 * 4
~tf0 = myArray`2[~t5]

~t6 = 1

~t7 = ~t6 * 1

~t8 = ~t7 * 4
~tf1 = myArray`2[~t8]

~tf2 = ~tf0 + ~tf1

~tf3 = (float) ~tf2
myArray`2[~t2] = ~tf3

#L6:
~t9 = 0

~t10 = ~t9 * 1

~t11 = ~t10 * 4

~t12 = 1

~t13 = ~t12 * 1

~t14 = ~t13 * 4
~tf5 = myArray`2[~t14]

~t15 = 0

~t16 = ~t15 * 1

~t17 = ~t16 * 4
~tf6 = myArray`2[~t17]

~tf4 = ~tf5 - ~tf6

~tf7 = (float) ~tf4
myArray`2[~t11] = ~tf7

#L4:
~t18 = 0

i`3 = (int) ~t18

#L13:

~t19 = 5

if i`3 < ~t19 goto #L14
goto #L11

#L14:


~t22 = i`3 * 1

~t23 = ~t22 * 4
output float, myArray`2[~t23]

#L15:


~t20 = 1

~t21 = i`3 + ~t20

i`3 = ~t21

goto #L13
#L11:

#L10:
return 

#L1:
