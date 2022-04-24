.data

.text
.globl main

fun2:
move $s8, $sp

addi $t0, $a0, 0
move $a0, $t0
li $v0, 1
syscall
li $t1, 0
sub $t2, $t0, $t1
beq $t2, $zero, _L13
j _L12
_L13:
move $sp, $s8
jr $ra
_L12:
li $t2, 1
sub $t3, $t0, $t2

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
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a0, $t3
jal fun2
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
lw $t2, -8($s8)
lw $t3, -12($s8)
move $sp, $s8
jr $ra
main:

move $s8, $sp

li $t0, 10
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
move $sp, $s8
jr $ra

