start:

int a[16]
a[0]=2
a[4]=3
a[8]=5
a[12]=34

L8:

t0 = 1 * 2
t1 = 1 * 1
t2 = t0 + t1

t3 = t2 * 4

t4 = (fuzzy) 2
a[t3] = t4

L6:

t5 = 1 * 2
t6 = 1 * 1
t7 = t5 + t6

t8 = t7 * 4

g = (int) a[t8]

L4:

a = 3

L2:

L1:
