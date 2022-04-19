.data
__t0:
	.asciiz "Hello, world!"

s__2:
	.ascii	"Hello, world!"
.text
.globl main

main:

move $s8, $sp

li $v0, 4
la $a0, s__2
syscall
move $sp, $s8
jr $ra

