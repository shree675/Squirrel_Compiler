.data

__t0:
	.asciiz "abcd"
.text
.globl main

main:

move $s8, $sp

la $t0, __t0
addi $t1, $t0, 0
li $v0, 4
la $a0, s__2
syscall
move $sp, $s8
jr $ra

