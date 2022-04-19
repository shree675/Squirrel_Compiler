.data
	a__2:
		.word 10, 11

.text
.globl main

main:

move $s8, $sp

li.s $f1, 21.5
cvt.w.s $t0, $f1
li $t1, 3
li $t2, 2
sub $t3, $t2, $t1
blt $t3, $zero, _L9
j _L8
_L9:
li $v0, 4
la $a0, __t2
syscall
_L8:
move $sp, $s8
jr $ra

