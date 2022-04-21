start:

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

~tf1 = 3.3

if ~tf0 == ~tf1 goto #L7
goto #L8

#L7:

~t3 = (int) 9
output int, ~t3

#L9:
goto #L6
#L8:
~t4 = 2

~t5 = ~t4 * 1

~t6 = ~t5 * 4
~tf2 = abc`2[~t6]

~tf3 = 4.4

if ~tf2 == ~tf3 goto #L11
goto #L12

#L11:

~t7 = (int) 10
output int, ~t7

#L13:
goto #L6
#L12:

~t8 = (int) 11
output int, ~t8

#L15:

#L6:
return 

#L1:
