.data
	arrx__2:
		.word 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6
	floatArray__2:
		.float 1.1, 2.2, 3.3, 4.4, 5.5, 6.6

.text
.globl main

main:

move $s8, $sp

li $t0, 0
addi $t1, $t0, 0
_L11:
li $t2, 4
sub $t3, $t1, $t2
blt $t3, $zero, _L12
j _L9
_L12:
li $t3, 0
addi $t4, $t3, 0
_L18:
li $t5, 3
sub $t6, $t4, $t5
blt $t6, $zero, _L19
j _L16
_L19:
li $t6, 0
addi $t7, $t6, 0
_L25:
li $s0, 2
sub $s1, $t7, $s0
blt $s1, $zero, _L26
j _L23
_L26:
li $s1, 0
li $s2, 6
mult $s1, $s2
mflo $s2
li $s3, 0
li $s4, 2
mult $s3, $s4
mflo $s4
add $s5, $s2, $s4
li $s6, 0
li $s7, 1
mult $s6, $s7
mflo $s7
add $t8, $s5, $s7
li $t9, 4
mult $t8, $t9
mflo $t9
lw $s1, arrx__2($t9)
move $a0, $s1
li $v0, 1
syscall
addi $sp, $sp, -4
sw $s1, 4($sp)
li $s1, 1
addi $sp, $sp, -4
sw $s3, 4($sp)
add $s3, $t7, $s1
addi $t7, $s3, 0
j _L25
_L23:
addi $sp, $sp, -4
sw $t4, 4($sp)
li $t4, 1
addi $sp, $sp, -4
sw $t4, 4($sp)
sw $t4, -12($s8)
lw $t4, -8($s8)
sw $t4, -8($s8)
lw $t4, -12($s8)
add $t4, $t4, $t4
addi $sp, $sp, -4
sw $t4, 4($sp)
addi $t4, $t4, 0
j _L18
_L16:
addi $sp, $sp, -4
sw $t1, 4($sp)
li $t1, 1
addi $sp, $sp, -4
sw $t1, 4($sp)
sw $t1, -24($s8)
lw $t1, -20($s8)
sw $t1, -20($s8)
lw $t1, -24($s8)
add $t1, $t1, $t1
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $t1, $t1, 0
j _L11
_L9:
move $sp, $s8
jr $ra

