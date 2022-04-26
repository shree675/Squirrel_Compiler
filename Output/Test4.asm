.data
	a__2:
		.word 1, 2, 3, 4, 5, 6, 7, 8, 9
	transpose__2:
		.word 0, 0, 0, 0, 0, 0, 0, 0, 0

__t24:
	.asciiz "\nTranspose of the matrix:\n"
__t40:
	.asciiz " "
__t41:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li $t0, 0
addi $t1, $t0, 0
_L15:
li $t2, 3
sub $t4, $t1, $t2
blt $t4, $zero, _L16
j _L13
_L16:
li $t3, 0
addi $t4, $t3, 0
_L22:
li $t5, 3
sub $t4, $t4, $t5
blt $t4, $zero, _L23
j _L20
_L23:
li $t6, 4
li $t7, 1
li $t8, 3
mult $t4, $t8
mflo $t9
mult $t1, $t7
mflo $s0
add $s1, $t9, $s0
mult $s1, $t6
mflo $s2
li $s3, 4
li $s4, 1
li $s5, 3
mult $t1, $s5
mflo $s6
mult $t4, $s4
mflo $s7
addi $sp, $sp, -4
sw $t6, 4($sp)
add $t6, $s6, $s7
addi $sp, $sp, -4
sw $t8, 4($sp)
mult $t6, $s3
mflo $t8
lw $t8, a__2($t8)
addi $sp, $sp, -4
sw $s0, 4($sp)
addi $s0, $t8, 0
sw $s0, transpose__2($s2)
addi $sp, $sp, -4
sw $s2, 4($sp)
li $s2, 1
addi $sp, $sp, -4
sw $s4, 4($sp)
add $s4, $t4, $s2
addi $t4, $s4, 0
j _L22
_L20:
addi $sp, $sp, -4
sw $t1, 4($sp)
li $t1, 1
addi $sp, $sp, -4
sw $t1, 4($sp)
lw $t1, -20($s8)
sw $t1, -24($s8)
add $t1, $t1, $t1
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $t1, $t1, 0
j _L15
_L13:
addi $sp, $sp, -4
sw $t9, 4($sp)
la $t9, __t24
li $v0, 4
la $a0, __t24
syscall
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 0
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
_L29:
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 3
addi $sp, $sp, -4
sw $t9, 4($sp)
lw $t9, -44($s8)
sub $t4, $t9, $t9
blt $t4, $zero, _L30
j _L27
_L30:
sw $t9, -44($s8)
li $t9, 0
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
_L38:
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 3
addi $sp, $sp, -4
sw $t9, 4($sp)
lw $t9, -56($s8)
sub $t4, $t9, $t9
blt $t4, $zero, _L39
j _L36
_L39:
sw $t9, -56($s8)
li $t9, 4
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 1
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 3
addi $sp, $sp, -4
sw $t9, 4($sp)
lw $t9, -44($s8)
sw $t9, -72($s8)
mult $t9, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
lw $t9, -56($s8)
sw $t9, -76($s8)
lw $t9, -68($s8)
sw $t9, -68($s8)
mult $t9, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
lw $t9, -76($s8)
sw $t9, -80($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
lw $t9, -64($s8)
sw $t9, -64($s8)
mult $t9, $t9
mflo $t9
lw $t9, transpose__2($t9)
move $a0, $t9
li $v0, 1
syscall
addi $sp, $sp, -4
sw $t9, 4($sp)
la $t9, __t40
li $v0, 4
la $a0, __t40
syscall
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 1
addi $sp, $sp, -4
sw $t9, 4($sp)
lw $t9, -56($s8)
sw $t9, -96($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
j _L38
_L36:
sw $t9, -56($s8)
la $t9, __t41
li $v0, 4
la $a0, __t41
syscall
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 1
addi $sp, $sp, -4
sw $t9, 4($sp)
lw $t9, -44($s8)
sw $t9, -108($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
j _L29
_L27:
move $sp, $s8
jr $ra

