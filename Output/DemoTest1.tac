start:
params 0

~t0 = 5

b`2 = (int) ~t0

#L44:
output int, b`2

#L42:
~t1 = (string) "\n"
output string, ~t1

#L40:
c`2 = (int) 0
#L38:

b2`2 = (bool) true

#L36:
~t2 = 0
~t3 = 1
if b2`2 == ~t2 goto #L46
output int, ~t3
goto #L47
#L46:
output int, ~t2
#L47:

#L34:
~t4 = (string) "\n"
output string, ~t4

#L32:
~t5 = "this is a test"

s`2 = (string) ~t5

#L30:
output string, s`2

#L28:
~t6 = (string) "\n"
output string, ~t6

#L26:


~t7 = b`2 - c`2

a`2 = (int) ~t7

#L24:

~t9 = 5

~t8 = a`2 * ~t9

d`2 = (float) ~t8

#L22:
~t10 = 10
~t11 = (char) ~t10

e`2 = (char) ~t11

#L20:
output int, a`2

#L18:
~t12 = (string) "\n"
output string, ~t12

#L16:
output int, b`2

#L14:
output int, c`2

#L12:




~t15 = b`2 + c`2

~t14 = a`2 / ~t15

~t16 = 6

~t13 = ~t14 % ~t16

a`2 = ~t13

#L10:
output int, a`2

#L8:
~t17 = (string) "\n"
output string, ~t17

#L6:

~t19 = 0
if a`2 == ~t19 goto #L50
if b`2 == ~t19 goto #L50
~t18 = true
goto #L49
#L50:
~t18 = false
#L49:

f`2 = (bool) ~t18

#L4:
~t20 = 0
~t21 = 1
if f`2 == ~t20 goto #L51
output int, ~t21
goto #L52
#L51:
output int, ~t20
#L52:

#L2:
return 

#L1:
