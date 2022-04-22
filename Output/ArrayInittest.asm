.data
	arr__2:
		.word 1, 2, 12, 5, 6, 7

.text
.globl main

main:

move $s8, $sp

li $t0, 0
li $t1, 2
mult $t0, $t1
mflo $t1
li $t2, 1
li $t3, 1
mult $t2, $t3
mflo $t3
add $t4, $t1, $t3
li $t5, 4
mult $t4, $t5
mflo $t5
li $t6, 2
li $t7, 2
mult $t6, $t7
mflo $t7
li $s0, 1
li $s1, 1
mult $s0, $s1
mflo $s1
add $s2, $t7, $s1
li $s3, 4
mult $s2, $s3
mflo $s3
lw $s3, arr__2($s3)
li $s4, 0
li $s5, 2
mult $s4, $s5
mflo $s5
li $s6, 0
li $s7, 1
mult $s6, $s7
mflo $s7
add $t8, $s5, $s7
li $t9, 4
mult $t8, $t9
mflo $t9
lw $t9, arr__2($t9)
addi $sp, $sp, -4
sw $t1, 4($sp)
sw $t1, 0($s8)
lw $t1, 4($s8)
addi $sp, $sp, -4
sw $t3, 4($sp)
lw $t3, 4($s8)
add $t1, $t1, $t3
addi $sp, $sp, -4
sw $t5, 4($sp)
addi $t5, $t1, 0
addi $sp, $sp, -4
sw $t7, 4($sp)
lw $t7, -8($s8)
sw $t5, arr__2($t7)
sw $t7, -8($s8)
li $t7, 0
addi $sp, $sp, -4
sw $s1, 4($sp)
sw $s1, -16($s8)
li $s1, 2
li $s1, 2
mult $t7, $s1
mflo $s1
addi $sp, $sp, -4
sw $s3, 4($sp)
li $s3, 1
addi $sp, $sp, -4
sw $s4, 4($sp)
sw $s4, -24($s8)
li $s4, 1
li $s4, 1
mult $s3, $s4
mflo $s4
addi $sp, $sp, -4
sw $s6, 4($sp)
add $s6, $s1, $s4
addi $sp, $sp, -4
sw $t8, 4($sp)
sw $t8, -32($s8)
li $t8, 4
li $t8, 4
mult $s6, $t8
mflo $t8
lw $t3, arr__2($t8)
move $a0, $t3
li $v0, 1
syscall
move $sp, $s8
jr $ra

