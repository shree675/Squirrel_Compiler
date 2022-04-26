start:
params 0

~tf0 = 0.0

i`2 = (float) ~tf0

#L16:
~tf1 = 0.0

j`2 = (float) ~tf1

#L14:
~tf2 = 0.0

k`2 = (float) ~tf2

#L12:
~tf3 = 0.0

l`2 = (float) ~tf3

# --------------

#L10:
~t0 = 0

count`2 = (int) ~t0

#L8:
#L18:

~tf4 = 2.0

# ------------------- 3

if j`2 < ~tf4 goto #L19
goto #L6

#L19:


~tf5 = 0.0

i`2 = ~tf5

#L24:
#L26:

~tf6 = 2.0

# ----------------- 4

if i`2 < ~tf6 goto #L27
goto #L22

#L27:


~tf7 = 0.0

k`2 = ~tf7

#L32:
#L34:

~tf8 = 10.0

if k`2 < ~tf8 goto #L35
goto #L30

#L35:

# ------------------ 5
~tf9 = 0.0

l`2 = ~tf9

#L40:
#L42:

~tf10 = 3.0

if l`2 < ~tf10 goto #L43
goto #L38

#L43:



~t1 = 1

~t2 = count`2 + ~t1

count`2 = ~t2

#L50:
output int, count`2

#L48:
~t3 = (string) "\n"
output string, ~t3

#L46:


~tf11 = 1.0

~tf12 = l`2 + ~tf11

l`2 = ~tf12

#L44:
goto #L42
#L38:


~tf13 = 1.0

~tf14 = k`2 + ~tf13

k`2 = ~tf14

#L36:
goto #L34
#L30:


~tf15 = 1.0

~tf16 = i`2 + ~tf15

i`2 = ~tf16

#L28:
goto #L26
#L22:


~tf17 = 1.0

~tf18 = j`2 + ~tf17

j`2 = ~tf18

#L20:
goto #L18
#L6:
~t4 = 3

a`2 = (int) ~t4

#L4:
~tf19 = 0.2

f`2 = (float) ~tf19

#L2:
return 

#L1:
