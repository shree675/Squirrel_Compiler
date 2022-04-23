.data

__t13:
	.asciiz "\n"
.text
.globl main

fibonacci:
move $s8, $sp

addi $t0, $a0, 0
li $t1, 0
sub $t2, $t0, $t1
beq $t2, $zero, _L7
j _L8
_L7:
li $t2, 0
move $sp, $s8
move $v0, $t2
jr $ra
jr $ra
_L8:
li $t3, 1
sub $t4, $t0, $t3
beq $t4, $zero, _L11
j _L12
_L11:
li $t4, 1
move $sp, $s8
move $v0, $t4
jr $ra
jr $ra
_L12:
li $t5, 1
sub $t6, $t0, $t5

# -------------------------------- 
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $sp, $sp, -4
sw $t3, 4($sp)
addi $sp, $sp, -4
sw $t4, 4($sp)
addi $sp, $sp, -4
sw $t5, 4($sp)
addi $sp, $sp, -4
sw $t6, 4($sp)
addi $sp, $sp, -4
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a0, $t6
jal fibonacci
move $t7, $v0
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
lw $t2, -8($s8)
lw $t3, -12($s8)
lw $t4, -16($s8)
lw $t5, -20($s8)
lw $t6, -24($s8)
li $s0, 2
sub $s1, $t0, $s0

# -------------------------------- 
sw $t0, 0($s8)
sw $t1, -4($s8)
sw $t2, -8($s8)
sw $t3, -12($s8)
sw $t4, -16($s8)
sw $t5, -20($s8)
sw $t6, -24($s8)
addi $sp, $sp, -4
sw $t7, 4($sp)
addi $sp, $sp, -4
sw $s0, 4($sp)
addi $sp, $sp, -4
sw $s1, 4($sp)
addi $sp, $sp, -4
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a0, $s1
jal fibonacci
move $s2, $v0
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
lw $t2, -8($s8)
lw $t3, -12($s8)
lw $t4, -16($s8)
lw $t5, -20($s8)
lw $t6, -24($s8)
lw $t7, -36($s8)
lw $s0, -40($s8)
lw $s1, -44($s8)
add $s3, $t7, $s2
addi $s4, $s3, 0
move $sp, $s8
move $v0, $s4
jr $ra
jr $ra
main:

move $s8, $sp

li $t0, 3
addi $t1, $t0, 0

# -------------------------------- 
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $sp, $sp, -4
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a0, $t1
jal fibonacci
move $t2, $v0
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
addi $t3, $t2, 0
move $a0, $t3
li $v0, 1
syscall
la $t4, __t13
li $v0, 4
la $a0, __t13
syscall
move $sp, $s8
jr $ra

