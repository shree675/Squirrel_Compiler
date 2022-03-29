start:

t|1 = - 1

t|0 = t|1 / 5

b = (int) t|0

L12:

t|2 = 1 - 2

d = (int) t|2

L10:

t|3 = d - b

f = (int) t|3

L8:

t|5 = - d

t|4 = t|5 - b

c = (int) t|4

L6:

t|7 = - b

t|6 = - t|7

e = (int) t|6

L4:
ifFalse d == 'a' goto L15
b = (int) 0
L16:
L15:

L14:
return 

L1:
