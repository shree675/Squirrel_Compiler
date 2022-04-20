.data
	arr__2:
		.word 1, 2

.text
.globl main

main:

move $s8, $sp

li $t0, 1
mult $t0, $t1
mflo $t1
mult $t1, $t2
mflo $t2
li $t3, 8
addi $t4, $t3, 0
sw $t4, arr__2($t2)
li $t5, 0
mult $t5, $t6
mflo $t6
mult $t6, $t7
mflo $t7
li $v0, 1
move $a0, $s0
syscall
li $s0, 1
mult $s0, $s1
mflo $s1
mult $s1, $s2
mflo $s2
li $v0, 1
move $a0, $s3
syscall
move $sp, $s8
jr $ra

