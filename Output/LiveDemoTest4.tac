start:

n = (int) 0
L10:
input int, n

L8:

sum = (float) 141.8

L6:

i = (int) 0

L15:

if i < n goto L16
goto L13

L16:

tf|1 = (float) i
tf|0 = sum + tf|1

sum = tf|0

L17:

t|0 = i + 1

i = t|0

goto L15
L13:

L12:

tf|3 = (float) 2
tf|2 = tf|3 * 141.8

if sum > tf|2 goto L20
goto L21

L20:

output float, sum

L22:
goto L19
L21:

if sum == 141.8 goto L24
goto L25

L24:

output float, 141.8

L26:
goto L19
L25:

tf|5 = (float) 1
tf|4 = sum + tf|5

temp = (float) tf|4

L30:
output float, temp

L28:

L19:
return 

L1:
