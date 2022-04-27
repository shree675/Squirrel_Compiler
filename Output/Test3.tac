start:
params 0

trial1`2 = (char) '0'
#L16:
trial2`2 = (char) '0'
#L14:
<<<<<<< HEAD
~t0 = (string) "H/h for head, T/t for tail\n"
=======
~t0 = (string) "H for head, T for tail\n"
>>>>>>> final
output string, ~t0

#L12:
~t1 = (string) "Enter the first outcome: "
output string, ~t1

#L10:
input char, trial1`2

#L8:
~t2 = (string) "Enter the second outcome: "
output string, ~t2

#L6:
input char, trial2`2

#L4:
~t6 = (char) 'H'
ifFalse trial1`2 == ~t6 goto #L19

~t4 = (char) 'H'
ifFalse trial2`2 == ~t4 goto #L25

~t3 = (string) "2 Heads\n"
output string, ~t3

#L28:
goto #L24
#L26:
#L25:


~t5 = (string) "Head and Tail\n"
output string, ~t5

#L30:
goto #L24

#L24:
goto #L18
#L20:
#L19:


~t8 = (char) 'H'
ifFalse trial2`2 == ~t8 goto #L35

~t7 = (string) "Tail and Head\n"
output string, ~t7

#L38:
goto #L34
#L36:
#L35:


~t9 = (string) "2 Tails\n"
output string, ~t9

#L40:
goto #L34

#L34:
goto #L18

#L18:
return 

#L1:
