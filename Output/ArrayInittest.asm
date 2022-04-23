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
addi $t8, $s7, 0
sw $t8, arr__2($s1)
li $t9, 0
addi $sp, $sp, -4
sw $t0, 4($sp)
sw $t0, 0($s8)
li $t0, 2
li $t0, 2
mult $t9, $t0
mflo $t0
addi $sp, $sp, -4
sw $t2, 4($sp)
li $t2, 1
addi $sp, $sp, -4
sw $t4, 4($sp)
sw $t4, -8($s8)
li $t4, 1
li $t4, 1
mult $t2, $t4
mflo $t4
addi $sp, $sp, -4
sw $t6, 4($sp)
add $t6, $t0, $t4
addi $sp, $sp, -4
sw $s0, 4($sp)
sw $s0, -16($s8)
li $s0, 4
li $s0, 4
mult $t6, $s0
mflo $s0
lw $s2, arr__2($s0)
move $a0, $s2
li $v0, 1
syscall
move $sp, $s8
jr $ra

