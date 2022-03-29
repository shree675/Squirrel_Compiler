intSum:

~t0 = a`2 + b`2

return ~t0
L5:
return 0

L4:

start:

int A`3[16]
A`3[0]=1
A`3[4]=-2
A`3[8]=3
A`3[12]=4

L15:
int B`3[16]
B`3[0]=9
B`3[4]=68
B`3[8]=7
B`3[12]=-60

L13:
int result`3[16]
result`3[0]=0
result`3[4]=0
result`3[8]=0
result`3[12]=0

L11:

i`3 = (int) 0

L9:
L17:

if i`3 < 2 goto L18
goto L7

L18:

j`5 = (int) 0

L28:

if j`5 < 2 goto L29
goto L26

L29:

~t2 = i`3 * 2
~t3 = j`5 * 1
~t4 = ~t2 + ~t3

~t5 = ~t4 * 4

~t6 = (int) 0
result`3[~t5] = ~t6

L36:

~t8 = i`3 * 2
~t9 = j`5 * 1
~t10 = ~t8 + ~t9

~t11 = ~t10 * 4

if result`3[~t11] != 0 goto L40
if 1 != 0 goto L40
~t7 = false
goto L39
L40:
~t7 = true
L39:

temp`5 = (int) ~t7

L34:

k`6 = (int) 0

L44:

if k`6 < 2 goto L45
goto L42

L45:

~t13 = i`3 * 2
~t14 = j`5 * 1
~t15 = ~t13 + ~t14

~t16 = ~t15 * 4

if result`3[~t16] < 0 goto L49
goto L50

L49:

~t17 = i`3 * 2
~t18 = j`5 * 1
~t19 = ~t17 + ~t18

~t20 = ~t19 * 4

~t21 = - 1

~t22 = (int) ~t21
result`3[~t20] = ~t22

L51:
goto L48
L50:

~t23 = i`3 * 2
~t24 = j`5 * 1
~t25 = ~t23 + ~t24

~t26 = ~t25 * 4

if result`3[~t26] == 0 goto L53
goto L54

L53:

~t27 = i`3 * 2
~t28 = j`5 * 1
~t29 = ~t27 + ~t28

~t30 = ~t29 * 4

~t31 = (int) 0
result`3[~t30] = ~t31

L55:
goto L48
L54:

~t33 = i`3 * 2
~t34 = k`6 * 1
~t35 = ~t33 + ~t34

~t36 = ~t35 * 4

~t37 = k`6 * 2
~t38 = j`5 * 1
~t39 = ~t37 + ~t38

~t40 = ~t39 * 4

~t32 = A`3[~t36] * B`3[~t40]

temp`5 = ~t32

L59:

~t41 = i`3 * 2
~t42 = j`5 * 1
~t43 = ~t41 + ~t42

~t44 = ~t43 * 4

~t46 = i`3 * 2
~t47 = j`5 * 1
~t48 = ~t46 + ~t47

~t49 = ~t48 * 4

L61:
param temp`5
param result`3[~t49]
~t45 = call intSum,2

result`3[~t44] = ~t45

L57:

L48:

~t12 = k`6 + 1

k`6 = ~t12

goto L44
L42:

L41:

~t50 = i`3 * 2
~t51 = j`5 * 1
~t52 = ~t50 + ~t51

~t53 = ~t52 * 4
output int, result`3[~t53]

L30:

~t1 = j`5 + 1

j`5 = ~t1

goto L28
L26:

L25:
output string, "\n"

L21:

~t54 = i`3 + 1

i`3 = ~t54

L19:
goto L17
L7:
return 

L2: