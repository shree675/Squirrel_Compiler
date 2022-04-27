start:
params 0

int a`2[36]
a`2[0] = 1
a`2[4] = 2
a`2[8] = 3
a`2[12] = 4
a`2[16] = 5
a`2[20] = 6
a`2[24] = 7
a`2[28] = 8
a`2[32] = 9

#L10:
int transpose`2[36]
transpose`2[0] = 0
transpose`2[4] = 0
transpose`2[8] = 0
transpose`2[12] = 0
transpose`2[16] = 0
transpose`2[20] = 0
transpose`2[24] = 0
transpose`2[28] = 0
transpose`2[32] = 0

#L8:
~t0 = 0

i`3 = (int) ~t0

#L15:

~t1 = 3

if i`3 < ~t1 goto #L16
goto #L13

#L16:

~t4 = 0

j`4 = (int) ~t4

#L22:

~t5 = 3

if j`4 < ~t5 goto #L23
goto #L20

#L23:


~t8 = j`4 * 3
~t9 = i`3 * 1
~t10 = ~t8 + ~t9

~t11 = ~t10 * 4


~t12 = i`3 * 3
~t13 = j`4 * 1
~t14 = ~t12 + ~t13

~t15 = ~t14 * 4
~t16 = a`2[~t15]

~t17 = (int) ~t16
transpose`2[~t11] = ~t17

#L24:


~t6 = 1

~t7 = j`4 + ~t6

j`4 = ~t7

goto #L22
#L20:

#L19:


~t2 = 1

~t3 = i`3 + ~t2

i`3 = ~t3

goto #L15
#L13:

#L12:
~t18 = (string) "\nTranspose of the matrix:\n"
output string, ~t18

#L4:
~t19 = 0

i`5 = (int) ~t19

#L29:

~t20 = 3

if i`5 < ~t20 goto #L30
goto #L27

#L30:

~t23 = 0

j`6 = (int) ~t23

#L38:

~t24 = 3

if j`6 < ~t24 goto #L39
goto #L36

#L39:


~t27 = i`5 * 3
~t28 = j`6 * 1
~t29 = ~t27 + ~t28

~t30 = ~t29 * 4
output int, transpose`2[~t30]

#L42:
~t31 = (string) " "
output string, ~t31

#L40:


~t25 = 1

~t26 = j`6 + ~t25

j`6 = ~t26

goto #L38
#L36:

#L35:
~t32 = (string) "\n"
output string, ~t32

#L31:


~t21 = 1

~t22 = i`5 + ~t21

i`5 = ~t22

goto #L29
#L27:

#L26:
return 

#L1:
