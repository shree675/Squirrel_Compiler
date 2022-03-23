start:

int a[16]
a[0]=2
a[4]=3
a[8]=5
a[12]=34

L10:

t0 = 1 * 2
t1 = 1 * 1
t2 = t0 + t1

t3 = t2 * 4

t4 = (int) 2
a[t3] = t4

L8:

t5 = 1 * 2
t6 = 1 * 1
t7 = t5 + t6

t8 = t7 * 4

g = (int) a[t8]

L6:
i = (int) 0
L4:

t9 = i * 2
t10 = 2 * 1
t11 = t9 + t10

t12 = t11 * 4

t13 = (int) 3
a[t12] = t13

L2:

L1:
