.data

__t1:
	.asciiz "\n"
__t4:
	.asciiz "\n"
__t5:
	.asciiz "this is a test"
__t6:
	.asciiz "\n"
__t12:
	.asciiz "\n"
__t17:
	.asciiz "\n"
s__2:
	.asciiz "this is a test"
.text
.globl main

main:

move $s8, $sp

li $t0, 5
addi $t1, $t0, 0
move $a0, $t1
li $v0, 1
syscall
la $t2, __t1
li $v0, 4
la $a0, __t1
syscall
li $t3, 0
li $t7, 1
li $t8, 0
li $t9, 1
move $t4, $t7
move $t5, $t8
move $a0, $t9
li $v0, 1
syscall
j _L47
_L46:
move $a0, $t8
li $v0, 1
syscall
_L47:
la $s0, __t4
li $v0, 4
la $a0, __t4
syscall
la $s1, __t5
addi $s2, $s1, 0
li $v0, 4
la $a0, s__2
syscall
la $s3, __t6
li $v0, 4
la $a0, __t6
syscall
sub $s4, $t1, $t3
addi $s5, $s4, 0
li $s6, 5
mult $s5, $s6
mflo $s7
mtc1 $s7, $f1
cvt.s.w $f3, $f1
addi $sp, $sp, -4
sw $s0, 4($sp)
li $s0, 10
addi $sp, $sp, -4
sw $s7, 4($sp)
addi $s7, $s0, 0
addi $sp, $sp, -4
sw $s0, 4($sp)
addi $s0, $s7, 0
move $a0, $s5
li $v0, 1
syscall
addi $sp, $sp, -4
sw $s7, 4($sp)
la $s7, __t12
li $v0, 4
la $a0, __t12
syscall
move $a0, $t1
li $v0, 1
syscall
move $a0, $t3
li $v0, 1
syscall
addi $sp, $sp, -4
sw $s7, 4($sp)
add $s7, $t1, $t3
addi $sp, $sp, -4
sw $s7, 4($sp)
div $s5, $s7
mflo $s7
addi $sp, $sp, -4
sw $s7, 4($sp)
li $s7, 6
addi $sp, $sp, -4
sw $s7, 4($sp)
lw $s7, -24($s8)
sw $s7, -28($s8)
div $s7, $s7
mfhi $s7
addi $s5, $s7, 0
move $a0, $s5
li $v0, 1
syscall
addi $sp, $sp, -4
sw $s7, 4($sp)
la $s7, __t17
li $v0, 4
la $a0, __t17
syscall
addi $sp, $sp, -4
sw $s7, 4($sp)
li $s7, 0
move $t4, $s5
move $t5, $s7
move $t4, $t1
move $t5, $s7
addi $sp, $sp, -4
sw $s7, 4($sp)
li $s7, 1
j _L49
_L50:
li $s7, 0
_L49:
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $s7, 0
bne $t9, $zero, ___L0
addi $t9, $zero, 0
j ___L1
___L0:
addi $t9, $zero, 1
___L1:
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 0
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 1
lw $t4, -48($s8)
lw $t5, -52($s8)
move $a0, $t9
li $v0, 1
syscall
j _L52
_L51:
addi $sp, $sp, -4
sw $t9, 4($sp)
lw $t9, -52($s8)
move $a0, $t9
li $v0, 1
syscall
_L52:
move $sp, $s8
jr $ra

