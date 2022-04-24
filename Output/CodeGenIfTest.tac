start:
params 0

float abc`2[16]
abc`2[0] = 1.1
abc`2[4] = 2.2
abc`2[8] = 3.3
abc`2[12] = 4.4

#L4:
~t0 = 2

~t1 = ~t0 * 1

~t2 = ~t1 * 4
~tf0 = abc`2[~t2]
~t3 = (bool) ~tf0


~t4 = (int) ~t3
~t5 = (int) true
if ~t4 == ~t5 goto #L7
goto #L8

#L7:

~t6 = (int) 9
output int, ~t6

#L9:
goto #L6
#L8:
~t7 = 2

~t8 = ~t7 * 1

~t9 = ~t8 * 4
~tf1 = abc`2[~t9]
~t10 = (int) ~tf1

~t11 = 3

~t12 = (int) ~t10
if ~t12 == ~t11 goto #L11
goto #L12

#L11:

~t13 = (int) 10
output int, ~t13

#L13:
goto #L6
#L12:

~t14 = (int) 11
output int, ~t14

#L15:

#L6:
return 

#L1:
