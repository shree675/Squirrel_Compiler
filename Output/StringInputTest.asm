.data

s5__2:
	.space 11
.text
.globl main

main:

move $s8, $sp

la $t0, s5__2
li $v0, 8
la $a0, s5__2
syscall
li $v0, 4
la $a0, s5__2
syscall
move $sp, $s8
jr $ra

