intMax:

if a >= b goto L8
goto L9

L8:

return a
L10:
goto L7
L9:

return b
L12:

L7:
return 0

L4:

start:

int arr[24]
arr[0]=-1
arr[4]=2
arr[8]=3
arr[12]=-4
arr[16]=5
arr[20]=6

L26:
float floatArr[8]
floatArr[0]=8.2
floatArr[4]=-2.5

L24:
char charArray[3]
charArray[0]='a'
charArray[1]='b'
charArray[2]='c'

L22:
i = (int) 0
L20:
j = (int) 0
L18:
k = (int) 0
L16:

t0 = i * 3
t1 = j * 1
t2 = t0 + t1
t3 = k * 1
t4 = t2 + t3

t5 = t4 * 4

L28:
param j
param 2
t6 = call intMax,2

arr[t5] = t6

L14:
return 

L2: