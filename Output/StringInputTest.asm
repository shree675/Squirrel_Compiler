.data

s__2:
	.space 10
.text
.globl main

main:

move $s8, $sp

li $v0, 8
la $a0, s__2
syscall
li $v0, 4
la $a0, s__2
syscall
move $sp, $s8
jr $ra

