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

<<<<<<< HEAD
~t14 = 4
~t12 = 1
~t8 = 3

~t9 = j`4 * ~t8
~t10 = i`3 * ~t12
~t11 = ~t9 + ~t10

~t13 = ~t11 * ~t14

~t21 = 4
~t19 = 1
~t15 = 3

~t16 = i`3 * ~t15
~t17 = j`4 * ~t19
~t18 = ~t16 + ~t17

~t20 = ~t18 * ~t21
~t22 = a`2[~t20]

~t23 = (int) ~t22
transpose`2[~t13] = ~t23
=======

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
>>>>>>> final

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
<<<<<<< HEAD
~t24 = (string) "\nTranspose of the matrix:\n"
output string, ~t24

#L4:
~t25 = 0

i`5 = (int) ~t25

#L29:

~t26 = 3

if i`5 < ~t26 goto #L30
=======
~t18 = (string) "\nTranspose of the matrix:\n"
output string, ~t18

#L4:
~t19 = 0

i`5 = (int) ~t19

#L29:

~t20 = 3

if i`5 < ~t20 goto #L30
>>>>>>> final
goto #L27

#L30:

<<<<<<< HEAD
~t29 = 0

j`6 = (int) ~t29

#L38:

~t30 = 3

if j`6 < ~t30 goto #L39
=======
~t23 = 0

j`6 = (int) ~t23

#L38:

~t24 = 3

if j`6 < ~t24 goto #L39
>>>>>>> final
goto #L36

#L39:

<<<<<<< HEAD
~t39 = 4
~t37 = 1
~t33 = 3

~t34 = i`5 * ~t33
~t35 = j`6 * ~t37
~t36 = ~t34 + ~t35

~t38 = ~t36 * ~t39
output int, transpose`2[~t38]

#L42:
~t40 = (string) " "
output string, ~t40
=======

~t27 = i`5 * 3
~t28 = j`6 * 1
~t29 = ~t27 + ~t28

~t30 = ~t29 * 4
output int, transpose`2[~t30]

#L42:
~t31 = (string) " "
output string, ~t31
>>>>>>> final

#L40:


<<<<<<< HEAD
~t31 = 1

~t32 = j`6 + ~t31

j`6 = ~t32
=======
~t25 = 1

~t26 = j`6 + ~t25

j`6 = ~t26
>>>>>>> final

goto #L38
#L36:

#L35:
<<<<<<< HEAD
~t41 = (string) "\n"
output string, ~t41
=======
~t32 = (string) "\n"
output string, ~t32
>>>>>>> final

#L31:


<<<<<<< HEAD
~t27 = 1

~t28 = i`5 + ~t27

i`5 = ~t28
=======
~t21 = 1

~t22 = i`5 + ~t21

i`5 = ~t22
>>>>>>> final

goto #L29
#L27:

#L26:
return 

#L1:
