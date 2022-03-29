start:

n`2 = (int) 0
L10:
input int, n`2

L8:

sum`2 = (float) 141.8

L6:

i`3 = (int) 0

L15:

if i`3 < n`2 goto L16
goto L13

L16:

~tf1 = (float) i`3
~tf0 = sum`2 + ~tf1

sum`2 = ~tf0

L17:

~t0 = i`3 + 1

i`3 = ~t0

goto L15
L13:

L12:

~tf3 = (float) 2
~tf2 = ~tf3 * 141.8

if sum`2 > ~tf2 goto L20
goto L21

L20:

output float, sum`2

L22:
goto L19
L21:

if sum`2 == 141.8 goto L24
goto L25

L24:

output float, 141.8

L26:
goto L19
L25:

~tf5 = (float) 1
~tf4 = sum`2 + ~tf5

temp`6 = (float) ~tf4

L30:
output float, temp`6

L28:

L19:
return 

L1:
