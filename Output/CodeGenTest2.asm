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
addi $t5, $t4, 0
li $t6, 0
mult $t6, $t7
mflo $t7
mult $t7, $s0
mflo $s0
lw $s0, arr__2($s0)
li $v0, 1
move $a0, $s0
syscall
li $s1, 1
mult $s1, $s2
mflo $s2
mult $s2, $s3
mflo $s3
lw $s3, arr__2($s3)
li $v0, 1
move $a0, $s3
syscall
move $sp, $s8
jr $ra

