start:

a`2 = (char) '0'
#L6:
b`2 = (float) 0.0
#L4:


~tf0 = (float) a`2
if ~tf0 <= b`2 goto #L9
goto #L8

#L9:



~tf2 = (float) a`2
~tf1 = ~tf2 + b`2

c`3 = (int) ~tf1

#L12:
output int, c`3

#L10:

#L8:
return 

#L1:
