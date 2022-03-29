printResult:

if value`2 != 0 goto L11
goto L10
L10:

output string, "It's not a palindrome"

L12:
goto L9
L11:

output string, "It's a palindrome"

L14:

L9:

return 0
L5:
return 0

L4:

start:

char array`5[4]
array`5[0]='a'
array`5[1]='b'
array`5[2]='x'
array`5[3]='b'

L28:

is_palindrome`5 = (bool) true

L26:

~t1 = (int)is_palindrome`5
if ~t1 != 0 goto L32
if 0 != 0 goto L32
~t0 = false
goto L31
L32:
~t0 = true
L31:

i`5 = (int) ~t0

L24:
input int, i`5

L22:

j`5 = (int) 3

L20:
L33:

if i`5 <= j`5 goto L34
goto L18

L34:

~t2 = i`5 * 1

~t3 = ~t2 * 1

~t4 = j`5 * 1

~t5 = ~t4 * 1

~t6 = (int)array`5[~t3]
~t7 = (int)array`5[~t5]
if ~t6 != ~t7 goto L42
goto L41

L42:

is_palindrome`5 = false

L45:
goto L33
L43:

L41:

~t8 = i`5 + 1

i`5 = ~t8

L37:

~t9 = j`5 - 1

j`5 = ~t9

L35:
goto L33
L18:

param is_palindrome`5
~t10 = call printResult,1

L16:
return 

L2: