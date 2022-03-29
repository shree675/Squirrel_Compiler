intMax:

if a`2 >= b`2 goto L8
goto L9

L8:

return a`2
L10:
goto L7
L9:

return b`2
L12:

L7:
return 0

L4:

start:

int arr`5[24]
arr`5[0]=-1
arr`5[4]=2
arr`5[8]=3
arr`5[12]=-4
arr`5[16]=5
arr`5[20]=6

L26:
float floatArr`5[8]
floatArr`5[0]=8.2
floatArr`5[4]=-2.5

L24:
char charArray`5[3]
charArray`5[0]='a'
charArray`5[1]='b'
charArray`5[2]='c'

L22:
i`5 = (int) 0
L20:
j`5 = (int) 0
L18:
k`5 = (int) 0
L16:

~t0 = i`5 * 3
~t1 = j`5 * 1
~t2 = ~t0 + ~t1
~t3 = k`5 * 1
~t4 = ~t2 + ~t3

~t5 = ~t4 * 4

L28:
param j`5
param 2
~t6 = call intMax,2

arr`5[~t5] = ~t6

L14:
return 

L2: