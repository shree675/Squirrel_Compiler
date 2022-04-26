start:
params 0

float abc`2[16]
abc`2[0] = 1.1
abc`2[4] = 2.2
abc`2[8] = 3.3
abc`2[12] = 4.4

#L4:
~t4 = 4
~t1 = 1
~t0 = 2

~t2 = ~t0 * ~t1

~t3 = ~t2 * ~t4
~tf0 = abc`2[~t3]
~t5 = (bool) ~tf0


~t6 = (int) ~t5
~t7 = (int) true
if ~t6 == ~t7 goto #L7
goto #L8

#L7:

~t8 = (int) 9
output int, ~t8

#L9:
goto #L6
#L8:
~t13 = 4
~t10 = 1
~t9 = 2

~t11 = ~t9 * ~t10

~t12 = ~t11 * ~t13
~tf1 = abc`2[~t12]
~t14 = (int) ~tf1

~t15 = 3

~t16 = (int) ~t14
if ~t16 == ~t15 goto #L11
goto #L12

#L11:

~t17 = (int) 10
output int, ~t17

#L13:
goto #L6
#L12:

~t18 = (int) 11
output int, ~t18

#L15:

#L6:
return 

#L1:
