start:

float floatArray`2[12]
floatArray`2[0] = 1.1
floatArray`2[4] = 5.0
floatArray`2[8] = 3.3

#L6:
~t0 = 2

~t1 = ~t0 * 1

~t2 = ~t1 * 4

~t3 = 1

~t4 = ~t3 * 1

~t5 = ~t4 * 4
~tf0 = floatArray`2[~t5]

~t6 = 0

~t7 = ~t6 * 1

~t8 = ~t7 * 4
~tf1 = floatArray`2[~t8]

~tf2 = ~tf0 + ~tf1

~tf3 = (float) ~tf2
floatArray`2[~t2] = ~tf3

#L4:
~t9 = 2

~t10 = ~t9 * 1

~t11 = ~t10 * 4
output float, floatArray`2[~t11]

#L2:
return 

#L1:
