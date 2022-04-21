.data

.text
.globl main

fun1:
move $s8, $sp

add $t0, $t0, $t1
addi $t2, $t0, 0
li $t3, 5
move $sp, $s8
move $v0, $t3
jr $ra
jr $ra
move $sp, $s8
move $v0, $t4
jr $ra
jr $ra
main:

move $s8, $sp

li $t0, 10
addi $t1, $t0, 0
li $t2, 1
addi $t3, $t2, 0
li $t4, 2
addi $t5, $t4, 0
li $t6, 3
addi $t7, $t6, 0

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
sw $t7, 4($sp)
addi $sp, $sp, -4
sw $ra, 4($sp)
addi $sp, $sp, -4
sw $s8, 4($sp)
move $a3, $t7
move $a2, $t5
move $a1, $t3
move $a0, $t1
jal fun1
move $s0, $v0
lw $s8, 4($sp)
lw $ra, 8($sp)
lw $t0, 0($s8)
lw $t1, -4($s8)
lw $t2, -8($s8)
lw $t3, -12($s8)
lw $t4, -16($s8)
lw $t5, -20($s8)
lw $t6, -24($s8)
lw $t7, -28($s8)
addi $t1, $s0, 0
move $sp, $s8
jr $ra

