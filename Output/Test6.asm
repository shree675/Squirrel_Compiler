.data
	a__2:
		.word 1, 2, 3, 4, 5, 6, 7, 8, 9
	b__2:
		.word 1, 2, 3, 4, 5, 6, 7, 8, 9
	c__2:
		.word 0, 0, 0, 0, 0, 0, 0, 0, 0

__t28:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li $t0, 0
addi $t1, $t0, 0
_L13:
li $t2, 9
sub $t3, $t1, $t2
blt $t3, $zero, _L14
j _L11
_L14:
li $t3, 3
div $t1, $t3
mflo $t4
addi $t5, $t4, 0
li $t6, 3
div $t1, $t6
mfhi $t7
addi $s0, $t7, 0
li $s1, 3
mult $t5, $s1
mflo $s1
li $s2, 1
mult $s0, $s2
mflo $s2
add $s3, $s1, $s2
li $s4, 4
mult $s3, $s4
mflo $s4
lw $s4, a__2($s4)
addi $s5, $s4, 0
li $s6, 3
mult $t5, $s6
mflo $s6
li $s7, 1
mult $s0, $s7
mflo $s7
add $t8, $s6, $s7
li $t9, 4
mult $t8, $t9
mflo $t9
lw $t9, b__2($t9)
addi $sp, $sp, -4
sw $t3, 4($sp)
addi $t3, $t9, 0
addi $sp, $sp, -4
sw $t7, 4($sp)
sw $t7, -4($s8)
li $t7, 3
li $t7, 3
mult $t5, $t7
mflo $t7
addi $sp, $sp, -4
sw $s1, 4($sp)
sw $s1, -8($s8)
li $s1, 1
li $s1, 1
mult $s0, $s1
mflo $s1
addi $sp, $sp, -4
sw $s3, 4($sp)
add $s3, $t7, $s1
sw $s4, 4($s8)
sw $s4, 4($s8)
li $s4, 4
li $s4, 4
mult $s3, $s4
mflo $s4
addi $sp, $sp, -4
sw $s6, 4($sp)
add $s6, $s5, $t3
addi $sp, $sp, -4
sw $t8, 4($sp)
addi $t8, $s6, 0
sw $t8, c__2($s4)
sw $t9, 4($s8)
sw $t9, 4($s8)
li $t9, 3
li $t9, 3
mult $t5, $t9
mflo $t9
addi $sp, $sp, -4
sw $t7, 4($sp)
sw $t7, -24($s8)
li $t7, 1
li $t7, 1
mult $s0, $t7
mflo $t7
addi $sp, $sp, -4
sw $s3, 4($sp)
add $s3, $t9, $t7
addi $sp, $sp, -4
sw $s6, 4($sp)
sw $s6, -32($s8)
li $s6, 4
li $s6, 4
mult $s3, $s6
mflo $s6
lw $s4, c__2($s6)
move $a0, $s4
li $v0, 1
syscall
addi $sp, $sp, -4
sw $s4, 4($sp)
la $s4, __t28
li $v0, 4
la $a0, __t28
syscall
addi $sp, $sp, -4
sw $t7, 4($sp)
li $t7, 1
addi $sp, $sp, -4
sw $s6, 4($sp)
add $s6, $t1, $t7
addi $t1, $s6, 0
j _L13
_L11:
move $sp, $s8
jr $ra

