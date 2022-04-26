start:
params 0

~t0 = 0

count`2 = (int) ~t0

#L4:
~t1 = 0

i`3 = (int) ~t1

#L9:

~t2 = 2

if i`3 < ~t2 goto #L10
goto #L7

#L10:

~t5 = 0

j`4 = (int) ~t5

#L16:

~t6 = 3

if j`4 < ~t6 goto #L17
goto #L14

#L17:

~t9 = 0

k`5 = (int) ~t9

#L23:

~t10 = 2

if k`5 < ~t10 goto #L24
goto #L21

#L24:

output int, count`2

#L29:
~t13 = (string) "\n"
output string, ~t13

#L27:


~t14 = 1

~t15 = count`2 + ~t14

count`2 = ~t15

#L25:


~t11 = 1

~t12 = k`5 + ~t11

k`5 = ~t12

goto #L23
#L21:

#L20:


~t7 = 1

~t8 = j`4 + ~t7

j`4 = ~t8

goto #L16
#L14:

#L13:


~t3 = 1

~t4 = i`3 + ~t3

i`3 = ~t4

goto #L9
#L7:

#L6:
return 

#L1:
