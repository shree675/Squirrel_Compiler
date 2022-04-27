.data
	arr__2:
		.float 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0

.text
.globl main

main:

move $s8, $sp

li $t0, 0
li $t1, 3
mult $t0, $t1
mflo $t1
li $t2, 0
li $t3, 1
mult $t2, $t3
mflo $t3
add $t4, $t1, $t3
li $t5, 4
mult $t4, $t5
mflo $t5
li $t6, 1
li $t7, 3
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
l.s $f3, arr__2($s3)
li $s4, 2
li $s5, 3
mult $s4, $s5
mflo $s5
li $s6, 2
li $s7, 1
mult $s6, $s7
mflo $s7
add $t8, $s5, $s7
li $t9, 4
mult $t8, $t9
mflo $t9
l.s $f4, arr__2($t9)
add.s $f5, $f3, $f4
mov.s $f6, $f5
s.s $f6, arr__2($t5)
addi $sp, $sp, -4
sw $t1, 4($sp)
li $t1, 0
addi $sp, $sp, -4
sw $t3, 4($sp)
sw $t3, -4($s8)
li $t3, 3
li $t3, 3
mult $t1, $t3
mflo $t3
addi $sp, $sp, -4
sw $t5, 4($sp)
li $t5, 0
addi $sp, $sp, -4
sw $t7, 4($sp)
sw $t7, -12($s8)
li $t7, 1
li $t7, 1
mult $t5, $t7
mflo $t7
addi $sp, $sp, -4
sw $s1, 4($sp)
add $s1, $t3, $t7
addi $sp, $sp, -4
sw $s4, 4($sp)
sw $s4, -20($s8)
li $s4, 4
li $s4, 4
mult $s1, $s4
mflo $s4
l.s $f7, arr__2($s4)
mov.s $f12, $f7
li $v0, 2
syscall
move $sp, $s8
jr $ra

