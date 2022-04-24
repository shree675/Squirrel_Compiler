.data

__t1:
	.asciiz "\n"
__t6:
	.asciiz "\n"
__t9:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li $t0, 97
mtc1 $t0, $f1
cvt.s.w $f3, $f1
mov.s $f12, $f3
li $v0, 2
syscall
la $t1, __t1
li $v0, 4
la $a0, __t1
syscall
li $t2, 97
addi $t3, $t2, 0
li $t4, 0
addi $t5, $t4, 0
li $t6, 0
li $t7, 1
sub $s0, $t3, $t6
beq $s0, $zero, _L20
move $a0, $t7
li $v0, 1
syscall
j _L21
_L20:
move $a0, $t6
li $v0, 1
syscall
_L21:
la $s0, __t6
li $v0, 4
la $a0, __t6
syscall
li $s1, 0
li $s2, 1
sub $s3, $t5, $s1
beq $s3, $zero, _L22
move $a0, $s2
li $v0, 1
syscall
j _L23
_L22:
move $a0, $s1
li $v0, 1
syscall
_L23:
la $s3, __t9
li $v0, 4
la $a0, __t9
syscall
move $sp, $s8
jr $ra

