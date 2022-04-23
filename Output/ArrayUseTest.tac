start:
params 0

int arrx`2[96]
arrx`2[0] = 1
arrx`2[4] = 2
arrx`2[8] = 3
arrx`2[12] = 4
arrx`2[16] = 5
arrx`2[20] = 6
arrx`2[24] = 1
arrx`2[28] = 2
arrx`2[32] = 3
arrx`2[36] = 4
arrx`2[40] = 5
arrx`2[44] = 6
arrx`2[48] = 1
arrx`2[52] = 2
arrx`2[56] = 3
arrx`2[60] = 4
arrx`2[64] = 5
arrx`2[68] = 6
arrx`2[72] = 1
arrx`2[76] = 2
arrx`2[80] = 3
arrx`2[84] = 4
arrx`2[88] = 5
arrx`2[92] = 6

#L6:
float floatArray`2[24]
floatArray`2[0] = 1.1
floatArray`2[4] = 2.2
floatArray`2[8] = 3.3
floatArray`2[12] = 4.4
floatArray`2[16] = 5.5
floatArray`2[20] = 6.6

#L4:
~t0 = 0

i`3 = (int) ~t0

#L11:

~t1 = 4

if i`3 < ~t1 goto #L12
goto #L9

#L12:

~t4 = 0

j`4 = (int) ~t4

#L18:

~t5 = 3

if j`4 < ~t5 goto #L19
goto #L16

#L19:

~t8 = 0

k`5 = (int) ~t8

#L25:

~t9 = 2

if k`5 < ~t9 goto #L26
goto #L23

#L26:

~t12 = 0

~t13 = ~t12 * 6
~t14 = 0
~t15 = ~t14 * 2
~t16 = ~t13 + ~t15
~t17 = 0
~t18 = ~t17 * 1
~t19 = ~t16 + ~t18

~t20 = ~t19 * 4
output int, arrx`2[~t20]

#L27:


~t10 = 1

~t11 = k`5 + ~t10

k`5 = ~t11

goto #L25
#L23:

#L22:


~t6 = 1

~t7 = j`4 + ~t6

j`4 = ~t7

goto #L18
#L16:

#L15:


~t2 = 1

~t3 = i`3 + ~t2

i`3 = ~t3

goto #L11
#L9:

#L8:
return 

#L1:
