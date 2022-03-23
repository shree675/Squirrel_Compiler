intSum:

t0 = a + b

return t0
L5:
return 0

L4:

start:

int A[16]
A[0]=1
A[4]=2
A[8]=3
A[12]=4

L15:
int B[16]
B[0]=9
B[4]=68
B[8]=7
B[12]=60

L13:
int result[16]
result[0]=0
result[4]=0
result[8]=0
result[12]=0

L11:

i = (int) 0

L9:
L17:

if i < 2 goto L18
goto L7

L18:

j = (int) 0

L28:

if j < 2 goto L29
goto L26

L29:

t2 = i * 2
t3 = j * 1
t4 = t2 + t3

t5 = t4 * 4

t6 = (int) 0
result[t5] = t6

L36:
temp = (int) 0
L34:

k = (int) 0

L41:

if k < 2 goto L42
goto L39

L42:

t8 = i * 2
t9 = j * 1
t10 = t8 + t9

t11 = t10 * 4

if result[t11] < 0 goto L46
goto L47

L46:

t12 = i * 2
t13 = j * 1
t14 = t12 + t13

t15 = t14 * 4

t16 = - 1

t17 = (int) t16
result[t15] = t17

L48:
goto L45
L47:

t18 = i * 2
t19 = j * 1
t20 = t18 + t19

t21 = t20 * 4

if result[t21] == 0 goto L50
goto L51

L50:

t22 = i * 2
t23 = j * 1
t24 = t22 + t23

t25 = t24 * 4

t26 = (int) 0
result[t25] = t26

L52:
goto L45
L51:

t28 = i * 2
t29 = k * 1
t30 = t28 + t29

t31 = t30 * 4

t32 = k * 2
t33 = j * 1
t34 = t32 + t33

t35 = t34 * 4

t27 = A[t31] * B[t35]

temp = t27

L56:

t36 = i * 2
t37 = j * 1
t38 = t36 + t37

t39 = t38 * 4

t41 = i * 2
t42 = j * 1
t43 = t41 + t42

t44 = t43 * 4

L58:
param temp
param result[t44]
t40 = call intSum,2

result[t39] = t40

L54:

L45:

t7 = k + 1

k = t7

goto L41
L39:

L38:

t45 = i * 2
t46 = j * 1
t47 = t45 + t46

t48 = t47 * 4
output int, result[t48]

L30:

t1 = j + 1

j = t1

goto L28
L26:

L25:
output string, "\n"

L21:

t49 = i + 1

i = t49

L19:
goto L17
L7:
return 

L2: