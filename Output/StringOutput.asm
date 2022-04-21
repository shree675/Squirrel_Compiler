.data

s__2:
	.asciiz "Hello, world!"
__t0:
	.asciiz "Hello, world!"
s1__2:
	.asciiz "Hello, world!"
s2__2:
	.asciiz "Hello, world!"
.text
.globl main

main:

move $s8, $sp

la $t0, s__2
la $t1, __t0
addi $t0, $t1, 0
addi $t2, $t0, 0
addi $t3, $t2, 0
li $v0, 4
la $a0, s__2
syscall
move $sp, $s8
jr $ra

