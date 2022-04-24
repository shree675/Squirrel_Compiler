start:
params 0

~tf0 = 0.0

i`2 = (float) ~tf0

#L10:
~tf1 = 0.0

j`2 = (float) ~tf1

#L8:
~tf2 = 0.0

k`2 = (float) ~tf2

#L6:
~tf3 = 0.0

l`2 = (float) ~tf3

#L4:
#L12:

~tf4 = 2.0

if j`2 < ~tf4 goto #L13
goto #L2

#L13:


~tf5 = 0.0

i`2 = ~tf5

#L20:
#L22:

~tf6 = 2.0

if i`2 < ~tf6 goto #L23
goto #L18

#L23:


~tf7 = 0.0

k`2 = ~tf7

#L30:
#L32:

~tf8 = 10.0

if k`2 < ~tf8 goto #L33
goto #L28

#L33:


~tf9 = 0.0

l`2 = ~tf9

#L40:
#L42:

~tf10 = 3.0

if l`2 < ~tf10 goto #L43
goto #L38

#L43:

~t0 = (int) l`2

x`6 = (int) ~t0

#L48:
output int, x`6

#L46:


~tf11 = 1.0

~tf12 = l`2 + ~tf11

l`2 = ~tf12

#L44:
goto #L42
#L38:
~t1 = (string) "\n"
output string, ~t1

#L36:


~tf13 = 1.0

~tf14 = k`2 + ~tf13

k`2 = ~tf14

#L34:
goto #L32
#L28:
~t2 = (string) "\n"
output string, ~t2

#L26:


~tf15 = 1.0

~tf16 = i`2 + ~tf15

i`2 = ~tf16

#L24:
goto #L22
#L18:
~t3 = (string) "\n"
output string, ~t3

#L16:


~tf17 = 1.0

~tf18 = j`2 + ~tf17

j`2 = ~tf18

#L14:
goto #L12
#L2:
return 

#L1:
