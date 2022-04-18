.text
.globl main

fun1:
move $s8, $sp

li $t0, 5
addi $t1, $t0, 0
move $sp, $s8
lw $v0, a__2
jr $ra
move $sp, $s8
lw $v0, 0
jr $ra
main:

move $s8, $sp

li $t0, 5
addi $t1, $t0, 0
li $t2, 5
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $t0, $t2, 0
addi $sp, $sp, -4
sw $t2, 4($sp)
li $t2, 5
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $t2, $t2, 0
addi $sp, $sp, -4
sw $t2, 4($sp)
li $t2, 5
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $t2, $t2, 0

# -------------------------------- 
addi $sp, $sp, -4
sw $t0, 4($sp)
addi $sp, $sp, -4
sw $t1, 4($sp)
addi $sp, $sp, -4
sw $t2, 4($sp)
addi $sp, $sp, -4
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a3, $t2
lw $a2, -12($s8)
move $a1, $t0
move $a0, $t1
jal fun
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, -20($s8)
lw $t1, -24($s8)
lw $t2, -28($s8)
sw $t2, -28($s8)
addi $t2, $t2, 0
move $sp, $s8
jr $ra

