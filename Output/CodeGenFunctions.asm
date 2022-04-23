.data

__t4:
	.asciiz "\n"
.text
.globl main

fun2:
move $s8, $sp

addi $t0, $a0, 0
move $a0, $t0
li $v0, 1
syscall
la $t1, __t4
li $v0, 4
la $a0, __t4
syscall
li $t2, 0
sub $t3, $t0, $t2
beq $t3, $zero, _L38
j _L37
_L38:
move $sp, $s8
jr $ra
_L37:
li $t3, 1
sub $t4, $t0, $t3

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
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a0, $t4
jal fun2
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
lw $t2, -8($s8)
lw $t3, -12($s8)
lw $t4, -16($s8)
move $sp, $s8
jr $ra
main:

move $s8, $sp

li $t0, 24
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
jal fun2
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
jr $ra

