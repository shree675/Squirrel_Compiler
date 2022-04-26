.data
	arr__2:
		.word 1, 2, 12, 5, 6, 7

.text
.globl main

main:

move $s8, $sp

li $t0, 2
addi $t1, $t0, 0
li $t2, 0
addi $t3, $t2, 0
li $t4, 0
li $t5, 2
mult $t4, $t5
mflo $t5
li $t6, 1
li $t7, 1
mult $t6, $t7
mflo $t7
add $s0, $t5, $t7
li $s1, 4
mult $s0, $s1
mflo $s1
li $s2, 2
mult $t1, $s2
mflo $s2
li $s3, 1
mult $t3, $s3
mflo $s3
add $s4, $s2, $s3
li $s5, 4
mult $s4, $s5
mflo $s5
lw $s5, arr__2($s5)
li $s6, 2
mult $s5, $s6
mflo $s7
add $t8, $s5, $s7
li $t9, 4
mult $t8, $t9
mflo $t9
lw $t9, arr__2($t9)
addi $sp, $sp, -4
sw $t0, 4($sp)
add $t0, $s3, $t9
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $t2, $t0, 0
sw $t2, arr__2($t5)
addi $sp, $sp, -4
sw $t4, 4($sp)
li $t4, 0
addi $sp, $sp, -4
sw $t6, 4($sp)
sw $t6, -12($s8)
li $t6, 2
li $t6, 2
mult $t4, $t6
mflo $t6
addi $sp, $sp, -4
sw $s0, 4($sp)
li $s0, 1
addi $sp, $sp, -4
sw $s2, 4($sp)
sw $s2, -20($s8)
li $s2, 1
li $s2, 1
mult $s0, $s2
mflo $s2
sw $s3, 4($s8)
add $s3, $t6, $s2
addi $sp, $sp, -4
sw $s5, 4($sp)
sw $s5, -24($s8)
li $s5, 4
li $s5, 4
mult $s3, $s5
mflo $s5
lw $s7, arr__2($s5)
move $a0, $s7
li $v0, 1
syscall
move $sp, $s8
jr $ra

