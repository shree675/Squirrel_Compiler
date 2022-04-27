.data
	a__2:
		.word 1, 2, 3, 4, 5, 6, 7, 8, 9
	transpose__2:
		.word 0, 0, 0, 0, 0, 0, 0, 0, 0

__t18:
	.asciiz "\nTranspose of the matrix:\n"
__t31:
	.asciiz " "
__t32:
	.asciiz "\n"
.text
.globl main

main:

move $s8, $sp

li $t0, 0
addi $t1, $t0, 0
_L15:
li $t2, 3
sub $t3, $t1, $t2
blt $t3, $zero, _L16
j _L13
_L16:
li $t3, 0
addi $t4, $t3, 0
_L22:
li $t5, 3
sub $t6, $t4, $t5
blt $t6, $zero, _L23
j _L20
_L23:
li $t6, 3
mult $t4, $t6
mflo $t6
li $t7, 1
mult $t1, $t7
mflo $t7
add $s0, $t6, $t7
li $s1, 4
mult $s0, $s1
mflo $s1
li $s2, 3
mult $t1, $s2
mflo $s2
li $s3, 1
mult $t4, $s3
mflo $s3
add $s4, $s2, $s3
li $s5, 4
mult $s4, $s5
mflo $s5
lw $s5, a__2($s5)
addi $s6, $s5, 0
sw $s6, transpose__2($s1)
li $s7, 1
add $t8, $t4, $s7
addi $t4, $t8, 0
j _L22
_L20:
li $t9, 1
addi $sp, $sp, -4
sw $t9, 4($sp)
add $t9, $t1, $t9
addi $t1, $t9, 0
j _L15
_L13:
addi $sp, $sp, -4
sw $t9, 4($sp)
la $t9, __t18
li $v0, 4
la $a0, __t18
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
sub $t9, $t9, $t9
blt $t9, $zero, _L30
j _L27
_L30:
sw $t9, -16($s8)
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
sub $t9, $t9, $t9
blt $t9, $zero, _L39
j _L36
_L39:
sw $t9, -28($s8)
sw $t9, -28($s8)
li $t9, 3
li $t9, 3
mult $t9, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -36($s8)
li $t9, 1
li $t9, 1
mult $t9, $t9
mflo $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -40($s8)
lw $t9, -40($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -44($s8)
li $t9, 4
li $t9, 4
mult $t9, $t9
mflo $t9
lw $t9, transpose__2($t9)
move $a0, $t9
li $v0, 1
syscall
addi $sp, $sp, -4
sw $t9, 4($sp)
la $t9, __t31
li $v0, 4
la $a0, __t31
syscall
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 1
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -56($s8)
lw $t9, -56($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
j _L38
_L36:
sw $t9, -28($s8)
la $t9, __t32
li $v0, 4
la $a0, __t32
syscall
addi $sp, $sp, -4
sw $t9, 4($sp)
li $t9, 1
addi $sp, $sp, -4
sw $t9, 4($sp)
sw $t9, -68($s8)
lw $t9, -68($s8)
add $t9, $t9, $t9
addi $sp, $sp, -4
sw $t9, 4($sp)
addi $t9, $t9, 0
j _L29
_L27:
move $sp, $s8
jr $ra

