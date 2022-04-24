.data
	cc__3:
		.byte 'a', 'b', 'c'

.text
.globl main

pp:
move $s8, $sp

addi $t0, $a0, 0
addi $t1, $a1, 0
addi $t2, $a2, 0
move $a0, $t0
li $v0, 11
syscall
move $a0, $t1
li $v0, 11
syscall
move $a0, $t2
li $v0, 11
syscall
move $sp, $s8
jr $ra


main:

move $s8, $sp

li $t0, 0
li $t1, 1
mult $t0, $t1
mflo $t1
li $t2, 1
mult $t1, $t2
mflo $t2
lw $t2, cc__3($t2)
li $t3, 1
li $t4, 1
mult $t3, $t4
mflo $t4
li $t5, 1
mult $t4, $t5
mflo $t5
lw $t5, cc__3($t5)
li $t6, 2
li $t7, 1
mult $t6, $t7
mflo $t7
li $s0, 1
mult $t7, $s0
mflo $s0
lw $s0, cc__3($s0)

# -------------------------------- 
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $sp, $sp, -4
sw $t1, 4($sp)
sw $t2, 4($s8)
addi $sp, $sp, -4
sw $t3, 4($sp)
addi $sp, $sp, -4
sw $t4, 4($sp)
sw $t5, 4($s8)
addi $sp, $sp, -4
sw $t6, 4($sp)
addi $sp, $sp, -4
sw $t7, 4($sp)
sw $s0, 4($s8)
addi $sp, $sp, -4
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a2, $s0
move $a1, $t5
move $a0, $t2
jal pp
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
lw $t2, 4($s8)
lw $t3, -8($s8)
lw $t4, -12($s8)
lw $t5, 4($s8)
lw $t6, -16($s8)
lw $t7, -20($s8)
lw $s0, 4($s8)
move $sp, $s8
jr $ra

